from __future__ import annotations

import asyncio
import os
import warnings
from collections.abc import Sequence
from datetime import datetime, timedelta
from json import JSONDecoder
from typing import Any, Literal

import attrs
from aiohttp import ClientSession
from aiohttp.client import _RequestOptions
from aiohttp.typedefs import StrOrURL
from aiohttp_client_cache import CachedSession, SQLiteBackend
from cachetools import Cache, LRUCache, TTLCache
from fake_useragent import UserAgent
from lxml import html
from selenium_driverless import webdriver
from selenium_driverless.scripts.network_interceptor import (
    InterceptedRequest,
    NetworkInterceptor,
    RequestPattern,
)
from shelved_cache import PersistentCache, cachedasyncmethod
from typing_extensions import Self

# NestedDictItem = (
#     dict[str, "NestedDictItem"]
#     | list["NestedDictItem"]
#     | str
#     | int
#     | float
#     | bool
#     | None
# )
# NestedDict = dict[str, NestedDictItem]
NestedDict = dict[str, Any]
Range1To24 = Literal[
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
]
Range1To100 = Literal[
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    88,
    89,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
    100,
]


# class ChromeClientSessionLike:
#     async def __aenter__(self) -> Self:
#         self.driver = await webdriver.Chrome().__aenter__()
#         return self

#     async def __aexit__(self, *args: Any) -> None:
#         await self.driver.__aexit__(*args)

#     def get(
#         self,
#         url: str,
#         callback: (
#             Callable[[webdriver.Chrome], Coroutine[None, None, None]] | None
#         ) = None,
#         **kwargs,
#     ) -> AsyncContextManager[str]:
#         @asynccontextmanager
#         async def _():
#             try:
#                 await self.driver.get(url)
#                 if callback is not None:
#                     await callback(self.driver)
#                 yield await self.driver.page_source
#             finally:
#                 await self.driver.quit()

#         return _()


@attrs.frozen
class ItemPrice:
    price: int
    maxPoint: int
    maxPointRatio: float
    bestCoupon: int
    realPrice: int

    @classmethod
    def from_itemScrape(cls, itemScrape: Sequence[NestedDict]) -> ItemPrice:
        dict_ = {}
        for item in itemScrape:
            dict_.update(item)
        price = dict_["props"]["pageProps"]["item"]["applicablePrice"]
        point_dict = dict_["props"]["pageProps"]["point"]
        maxPoint = point_dict["totalPoint"] + point_dict["moreTotalPoint"]
        maxPointRatio = (
            point_dict["totalPointRatio"] + point_dict["moreTotalPointRatio"]
        )
        try:
            bestCoupon = dict_["first_view_coupon"]["hotdeal"]["item_discount_price"]
        except KeyError:
            bestCoupon = 0
        realPrice = price - bestCoupon - maxPoint
        return cls(price, maxPoint, maxPointRatio, bestCoupon, realPrice)


class YahooShopping:
    next_request: datetime | None = None
    wait_time: float = 1.0
    cache: Cache[Any, Any]

    def __init__(
        self,
        *,
        appid: str | None | Literal[False] = None,
        session: ClientSession | None = None,
        driver: webdriver.Chrome | None | Literal[False] = None,
        cache: Cache[Any, Any] | None | Literal[False] = None,
    ) -> None:
        """Python wrapper for Yahoo! Shopping API.

        Parameters
        ----------
        appid : str | None, optional
            The application ID, by default None
            If None, it will try to get the appid from the environment variable "YAHOO_APP_ID".
            You can get the appid from https://e.developer.yahoo.co.jp/register.
        session : ClientSession | None, optional
            The aiohttp-compatible session, by default None
        driver : webdriver.Chrome | None | Literal[False], optional
            The selenium driver used to scrape the website, by default None
            If False, it will not use the selenium driver.
        """
        if appid is False:
            pass
        else:
            self.appid = appid or os.getenv("YAHOO_APP_ID")
            if self.appid is None:
                warnings.warn(
                    "The appid is not provided. You can get the appid"
                    " from https://e.developer.yahoo.co.jp/register"
                    "and set it as the environment variable 'YAHOO_APP_ID'.",
                    UserWarning,
                    stacklevel=2,
                )
        self.json_decoder = JSONDecoder()
        self.user_agent = UserAgent()
        self.session = session or CachedSession(
            backend=SQLiteBackend(cache_name="~/.cache/yahoo_shopping/main.sqlite"),
            headers={"User-Agent": self.user_agent.random},
        )
        self.session = session or ClientSession()
        if cache is False:
            self.cache = LRUCache(maxsize=0)
        else:
            self.cache = cache or PersistentCache(
                TTLCache,
                maxsize=1000,
                ttl=timedelta(hours=1).total_seconds(),
                filename="~/.cache/yahoo_shopping/browser_cache",
            )
        if driver is not False:
            self.driver = driver or webdriver.Chrome()

    async def __aenter__(self) -> Self:
        await self.session.__aenter__()
        if hasattr(self, "driver"):
            await self.driver.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.session.__aexit__(*args)
        if hasattr(self, "driver"):
            await self.driver.__aexit__(*args)

    async def fetch(self, url: StrOrURL, **kwargs: _RequestOptions) -> NestedDict:
        if self.next_request is not None and self.next_request > datetime.now():
            await asyncio.sleep((self.next_request - datetime.now()).total_seconds())
        self.next_request = datetime.now() + timedelta(seconds=self.wait_time)

        # remove None in kwargs
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        async with self.session.get(url, params=kwargs) as response:
            return await response.json()

    async def itemSearch(
        self,
        *,
        affiliate_type: str | None = None,
        affiliate_id: str | None = None,
        query: str | None = None,
        jan_code: str | None = None,
        image_size: Literal[76, 106, 132, 146, 300, 600] | None = None,
        genre_category_id: int | None = None,
        brand_id: int | None = None,
        seller_id: str | None = None,
        price_from: int | None = None,
        price_to: int | None = None,
        affiliate_rate_from: float | None = None,
        affiliate_rate_to: float | None = None,
        preorder: bool | None = None,
        results: Range1To100 | None = None,
        start: int | None = None,
        in_stock: bool | None = None,
        is_discounted: bool | None = None,
        shipping: str | None = None,
        payment: str | None = None,
        user_rank: (
            Literal["diamond", "platinum", "gold", "silver", "bronze", "guest"] | None
        ) = None,
        sale_end_from: int | None = None,
        sale_end_to: int | None = None,
        sale_start_from: int | None = None,
        sale_start_to: int | None = None,
        delivery_area: str | None = None,
        delivery_day: Literal[0, 1, 2] | None = None,
        delivery_deadline: Range1To24 | None = None,
        sort: Literal["-score", "+price", "-price", "-review_count"] | None = None,
        condition: Literal["new", "used"] | None = None,
        **kwargs: _RequestOptions,
    ) -> NestedDict:
        """
        パラメータ	必須	型	デフォルト値	例	説明
        appid	〇	string			Client ID（アプリケーションID）
        affiliate_type		string		vc	バリューコマースアフィリエイト（vc）を選択
        affiliate_id		string			バリューコマースアフィリエイトID
        query		string			UTF-8エンコードされた検索キーワード
        jan_code		string		4905524535815	JANコード
        image_size		integer		76	取得したい任意の画像サイズを指定できます。
        指定する値と画像サイズ
        76：76×76
        106：106×106
        132：132×132
        146：146×146
        300：300×300
        600：600×600
        genre_category_id		integer		2495	ジャンルカテゴリID
        カンマ区切りで複数指定できる
        複数指定した場合はOR絞り込みになる
        brand_id		integer		149	ブランドID
        カンマ区切りで複数指定できる
        複数指定した場合はOR絞り込みになる
        seller_id		string			ストアID
        price_from		integer		1000	商品価格 (下限) (下限は含む)
        price_to		integer		10000	商品価格 (上限) (上限は含む)
        affiliate_rate_from		float		10.0	アフィリエイト料率(下限)（下限は含む）
        affiliate_rate_to		float		20.0	アフィリエイト料率(上限)（上限は含む）
        preorder		boolean		true	予約商品の指定
        true：予約商品のみ
        results		integer	20	50	検索結果の返却数
        start		integer	1	31	返却結果の先頭位置
        例）31件目から欲しい場合は「31 」
        ※start + resultsの合計は1,000が上限
        in_stock		boolean		true	在庫有無
        true：在庫ありのみ
        false：在庫なしのみ
        is_discounted		boolean		true	セール対象商品に絞り込み
        shipping		string		free	送料区分の指定
        free：送料無料
        conditional_free：条件付き送料無料
        ※複数指定によるOR検索可
        payment		string			支払い方法
        1：クレジットカード
        2：銀行振込
        4：商品代引
        8：郵便振替
        16：Yahoo!ウォレット登録済みクレジットカード
        32：モバイルSuica
        64：コンビニ
        128：ペイジー
        256：ドコモケータイ払い
        512：auかんたん決済
        1024：ソフトバンク・ワイモバイルまとめて支払い
        4096：PayPay
        8192：ゆっくり払い
        16384：PayPayあと払い
        user_rank		string	guest	diamond	指定すると会員属性に応じたポイント額を返します。
        値：diamond/platinum/gold/silver/bronze/guest(デフォルト)
        sale_end_from		integer	now		販売終了UNIX時間の下限
        sale_end_to		integer			販売終了UNIX時間の上限
        sale_start_from		integer	0		販売開始UNIX時間の下限
        sale_start_to		integer	now + 7d		販売開始UNIX時間の上限
        delivery_area		string	string	08	きょうつく、あすつく、翌々日配送の都道府県の指定
        都道府県コードは下方を参照
        JIS都道府県コードに準拠するため、1桁の場合も頭に0を付けて2桁のstringで指定すること

        ※delivery_area, delivery_deadline, delivery_dayの3パラメータ全てが指定された場合にのみ絞り込みになる。
        delivery_areaのみ指定した場合は、絞り込みはしないが、レスポンスのDelivery配下が指定した都道府県の情報になる。
        delivery_day		integer		0	あすつく、きょうつく、翌々日配送の指定
        0：きょうつく
        1：あすつく
        2：翌々日配送
        delivery_deadline		integer		13	発送日の締め時間を指定
        ・24時間表記 (1〜24)で指定
        　integerで指定(01のようなstringはNG)
        　締め時間全てを指定する場合は1を指定 (1〜24)で全時間指定となる
        ・境界は含まれる
        　例）15　→ 15時〜24時が締め時間の当日配送可能商品で絞り込まれる
        ・99を指定した場合のみ現在時+1時間が入って絞りこまれる
        　例）14時20分 → 15時, 15時00分 → 16時
        sort		string	-score	+price	並び順を指定
        -score：おすすめ順
        +price：価格の安い順
        -price：価格の高い順
        -review_count：商品レビュー数の多い順
        ※UTF-8にエンコードされている必要あり。
        condition		string		new	商品状態の指定
        used: 中古
        new: 新品
        """
        return await self.fetch(
            "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch",
            **{
                "appid": self.appid,
                "affiliate_type": affiliate_type,
                "affiliate_id": affiliate_id,
                "query": query,
                "jan_code": jan_code,
                "image_size": image_size,
                "genre_category_id": genre_category_id,
                "brand_id": brand_id,
                "seller_id": seller_id,
                "price_from": price_from,
                "price_to": price_to,
                "affiliate_rate_from": affiliate_rate_from,
                "affiliate_rate_to": affiliate_rate_to,
                "preorder": preorder,
                "results": results,
                "start": start,
                "in_stock": in_stock,
                "is_discounted": is_discounted,
                "shipping": shipping,
                "payment": payment,
                "user_rank": user_rank,
                "sale_end_from": sale_end_from,
                "sale_end_to": sale_end_to,
                "sale_start_from": sale_start_from,
                "sale_start_to": sale_start_to,
                "delivery_area": delivery_area,
                "delivery_day": delivery_day,
                "delivery_deadline": delivery_deadline,
                "sort": sort,
                "condition": condition,
                **kwargs,
            },
        )

    async def highRatingTrendRanking(
        self,
        *,
        affiliate_type: str | None = None,
        affiliate_id: str | None = None,
        query: str | None = None,
        genre_category_id: list[int] | None = None,
        brand_id: list[int] | None = None,
        exclude_genre_category_id: list[int] | None = None,
        exclude_brand_id: list[int] | None = None,
        price_from: int | None = None,
        price_to: int | None = None,
        seller_id: list[str] | None = None,
        delivery: bool | None = None,
        app_ban: Literal[0, 1, 2] | None = None,
        offset: int | None = None,
        limit: Range1To100 | None = None,
        **kwargs: _RequestOptions,
    ) -> NestedDict:
        """
        パラメータ	型	説明
        appid
        （必須）	String	Client ID（アプリケーションID）。詳細はこちらをご覧ください。
        affiliate_type	String	バリューコマースアフィリエイト(vc)を選択。
        例：affiliate_type=vc
        affiliate_id	String	バリューコマースアフィリエイトID
        query	String	検索クエリ
        ※ 文字コードはUTF-8を想定しています。
        genre_category_id	Integer[]	ジャンルカテゴリID
        カンマ区切りで複数指定できます。
        複数指定の場合はOR検索です。
        ※ 複数指定の場合、上限は50カテゴリです。
        brand_id	Long[]	ブランドコード
        カンマ区切りで複数指定できます。
        複数指定の場合はOR検索です。
        ※ 複数指定の場合、上限は50ブランドです。
        exclude_genre_category_id	Integer[]	除外するジャンルカテゴリID
        除外するジャンルカテゴリIDを指定することで当該カテゴリを含む商品をランキングから排他します。
        複数のカテゴリを指定するとそれらを含む商品を全て排他します。
        ※ (NOT カテゴリA) AND (NOT カテゴリB)のようにANDで否定条件が結合されます。
        ※ 複数指定の場合、上限は50カテゴリです。
        exclude_brand_id	Long[]	除外するブランドコード
        除外するブランドコードを指定することで当該ブランドを含む商品をランキングから排他します。
        複数のブランドを指定するとそれらを含む商品を全て排他します。
        ※ (NOT ブランドA) AND (NOT ブランドB)のようにANDで否定条件が結合されます。
        ※ 複数指定の場合、上限は50ブランドです。
        price_from	Integer	商品価格（下限）
        ※ 下限を含みます。
        ※ セール期間の場合はセール価格を、セール期間外の場合は通常価格を検索します。
        ※ ストアが日中に設定変更した場合などずれが生じる場合があります。
        price_to	Integer	商品価格（上限）
        ※ 上限を含みます。
        ※ セール期間の場合はセール価格を、セール期間外の場合は通常価格を検索します。
        ※ ストアが日中に設定変更した場合などずれが生じる場合があります。
        seller_id	String[]	ストアアカウント（ストアID）
        カンマ区切りで複数指定できます。
        複数指定の場合はOR検索です。
        ※ 複数指定の場合、上限は50ストアです。
        delivery	Boolean	送料無料設定
        （true：送料無料の商品のみ、falseまたは未指定：全商品）
        app_ban	Integer	アプリ最適化設定
        ランキングに含まれる商品をエンドユーザのデバイスに応じて制御します。
        0：全商品掲出
        1：iOS用に掲出商品を最適化
        2：android用に掲出商品を最適化
        ※ デフォルト値は0です。
        offset	Integer	指定した順位からランキングを取得します。
        例）offset=1の場合1位からのランキングを取得、offset=11の場合11位からのランキングを取得します。
        ※ デフォルト値は1です。
        limit	Integer	ランキングの取得件数
        ※ 上限は100です。
        ※ デフォルト値は20です。
        """
        return await self.fetch(
            "https://shopping.yahooapis.jp/ShoppingWebService/V1/highRatingTrendRanking",
            **{
                "appid": self.appid,
                "affiliate_type": affiliate_type,
                "affiliate_id": affiliate_id,
                "query": query,
                "genre_category_id": genre_category_id,
                "brand_id": brand_id,
                "exclude_genre_category_id": exclude_genre_category_id,
                "exclude_brand_id": exclude_brand_id,
                "price_from": price_from,
                "price_to": price_to,
                "seller_id": seller_id,
                "delivery": delivery,
                "app_ban": app_ban,
                "offset": offset,
                "limit": limit,
                **kwargs,
            },
        )

    async def itemLookup(
        self,
        itemcode: str,
        *,
        affiliate_type: str | None = None,
        affiliate_id: str | None = None,
        callback: str | None = None,
        responsegroup: Literal["small", "medium", "large"] | None = None,
        image_size: Literal[76, 106, 132, 146, 300, 600] | None = None,
        license: (
            Literal["diamond", "platinum", "gold", "silver", "bronze", "guest"] | None
        ) = None,
        **kwargs: _RequestOptions,
    ) -> NestedDict:
        """
        パラメータ	値	説明
        appid
        （必須）	string	Client ID（アプリケーションID）。詳細はこちらをご覧ください。
        affiliate_type	vc	バリューコマースアフィリエイト（vc）を選択。
        例：affiliate_type=vc
        affiliate_id	string	バリューコマースアフィリエイトIDを入力。
        callback	string	JSONPとして出力する際のコールバック関数名を入力するためのパラメータ。UTF-8でエンコードした文字列を入力する。
        itemcode
        （必須）	string	商品コード（商品検索APIおよびカテゴリランキングAPIの結果リストのCodeタグに含まれる、商品固有のコード。ストアID_ストア商品コードの組み合わせ）
        responsegroup	small/medium/large	デフォルトはsmall。
        取得できるデータのサイズを指定できる。smallが最小、最速です。詳細はレスポンスフィールドに記載があります。
        image_size	76/106/132/146/300/600	取得したい任意の画像サイズを指定できます。
        指定する値と画像サイズ
        　76：76×76
        　106：106×106
        　132：132×132
        　146：146×146
        　300：300×300
        　600：600×600
        license	diamond/platinum/gold/silver/bronze/guest(デフォルト)	スタンプラリーの会員ランクを指定すると、それに応じたポイントを返します。デフォルトはguest。(responsegroupがmedium以上で有効)
        ※2010年10月1日以降のlicenseパラメータは無効となります。
        """
        return await self.fetch(
            "https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemLookup",
            **{
                "appid": self.appid,
                "itemcode": itemcode,
                "affiliate_type": affiliate_type,
                "affiliate_id": affiliate_id,
                "callback": callback,
                "responsegroup": responsegroup,
                "image_size": image_size,
                "license": license,
                **kwargs,
            },
        )

    async def categorySearch(
        self,
        *,
        affiliate_type: str | None = None,
        affiliate_id: str | None = None,
        callback: str | None = None,
        category_id: int,
    ) -> NestedDict:
        """
        パラメータ	値	説明
        appid（必須）	string	Client ID（アプリケーションID）。詳細はこちらをご覧ください。
        output	xml(デフォルト)/php/json/jsonp/	レスポンス形式の指定
        XMLのリクエストURL(shopping.yahooapis.jp/ShoppingWebService/V1/categorySearch)のみ使用可能で、 このパラメータを指定すると各形式でのレスポンスを返すことができます。
        未指定, xml：XML形式
        json, jsonp：JSON形式
        affiliate_type	vc	バリューコマースアフィリエイト(vc)を選択。
        例：affiliate_type=vc
        affiliate_id	string	バリューコマースアフィリエイトIDを入力。
        callback	string	JSONPとして出力する際のコールバック関数名を入力する為のパラメータ。UTF-8でエンコードした文字列を入力する。
        例：以下いずれの場合もJSONPで返します。
        https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categorySearch?callback=xxxxx
        https://shopping.yahooapis.jp/ShoppingWebService/V1/categorySearch?output=json&callback=xxxxx
        https://shopping.yahooapis.jp/ShoppingWebService/V1/categorySearch?output=jsonp&callback=xxxxx
        category_id（必須）	integer	カテゴリIDを指定。
        category_id=1のときルートカテゴリを返す(第1階層)。
        """
        return await self.fetch(
            "https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categorySearch",
            **{
                "appid": self.appid,
                "affiliate_type": affiliate_type,
                "affiliate_id": affiliate_id,
                "callback": callback,
                "category_id": category_id,
            },
        )

    async def queryRanking(
        self,
        *,
        affiliate_type: str | None = None,
        affiliate_id: str | None = None,
        type: Literal["ranking", "up"] | None = None,
        hits: Range1To100 | None = None,
        offset: int | None = None,
        category_id: int | None = None,
    ) -> NestedDict:
        """
                パラメータ	値	説明
        appid
        （必須）	string	Client ID（アプリケーションID）。詳細はこちらをご覧ください。
        affiliate_type	vc	バリューコマースアフィリエイト（vc）を選択。
        例：affiliate_type=vc
        affiliate_id	string	バリューコマースアフィリエイトIDを入力
        type	ranking/up	出力するコンテンツタイプを選択する。デフォルトはranking、rankingは検索キーワードランキング、upは急上昇した検索キーワードを返します。
        hits	integer	type=rankingのときにのみ有効、デフォルトは20件、最大100件。
        offset	integer	type=rankingのときにのみ有効、offset=0のとき1位～20位、offset=20だと21位～40位までの情報を返します。
        category_id	integer	指定したカテゴリID以下のキーワードランキング情報を返します　例category_id=2494
        """
        return await self.fetch(
            "https://shopping.yahooapis.jp/ShoppingWebService/V2/queryRanking",
            **{
                "appid": self.appid,
                "affiliate_type": affiliate_type,
                "affiliate_id": affiliate_id,
                "type": type,
                "hits": hits,
                "offset": offset,
                "category_id": category_id,
            },
        )

    async def getModule(
        self,
        position: Literal["querykeyword", "hotitem", "basicpromotion", "bestpromotion"],
        *,
        affiliate_type: str | None = None,
        affiliate_id: str | None = None,
        callback: str | None = None,
        category_id: int,
    ) -> NestedDict:
        """
        パラメータ	値	説明
        appid
        （必須）	string	Client ID（アプリケーションID）。詳細はこちらをご覧ください。
        affiliate_type	vc	バリューコマースアフィリエイト(vc)を選択。
        例：affiliate_type=vc
        affiliate_id	string	バリューコマースアフィリエイトIDを入力。
        callback	string	JSONPとして出力する際のコールバック関数名を入力するためのパラメータ。UTF-8でエンコードした文字列を入力する。
        category_id
        （デフォルト1）	integer	取得したいおすすめ情報モジュールがあるカテゴリ階層のカテゴリIDを指定します。
        position
        (必須）	トップページ（category_id=1）
        　・querykeyword
        　・hotitem

        カテゴリページ（category_id=1以外）
        　・basicpromotion
        　・bestpromotion	トップページ（category_id=1）の場合に以下のpositionを指定できます。
        　・querykeyword:検索人気キーワードをピックアップして紹介する情報。（更新頻度高）
        　・hotitem:話題情報の画像とキャッチコピーを掲載しているモジュール情報。（更新頻度中）

        カテゴリページの場合に以下のpositionを指定できます。
        　・basicpromotion:画像ありのおすすめ特集や商品のご紹介情報。
        　・bestpromotion:画像なしのおすすめ特集や商品のご紹介情報。
        """
        return await self.fetch(
            "https://shopping.yahooapis.jp/ShoppingWebService/V1/json/getModule",
            **{
                "appid": self.appid,
                "affiliate_type": affiliate_type,
                "affiliate_id": affiliate_id,
                "callback": callback,
                "category_id": category_id,
                "position": position,
            },
        )

    async def reviewSearch(
        self,
        *,
        affiliate_type: str | None = None,
        affiliate_id: str | None = None,
        callback: str | None = None,
        jan: int | None = None,
        category_id: int | None = None,
        product_id: str | None = None,
        person_id: int | None = None,
        store_id: str | None = None,
        results: int | None = None,
        start: int | None = None,
        sort: (
            Literal["-updatetime", "-review_rate", "+updatetime", "+review_rate"] | None
        ) = None,
    ) -> NestedDict:
        """
        パラメータ	値	説明
        appid
        （必須）	string	Client ID（アプリケーションID）。詳細はこちらをご覧ください。
        affiliate_type	vc	バリューコマースアフィリエイト（vc）を選択。
        例：affiliate_type=vc
        affiliate_id	string	バリューコマースアフィリエイトIDを入力。
        callback	string	JSONPとして出力する際のコールバック関数名を入力する為のパラメータ。UTF-8でエンコードした文字列を入力する。
        jan
        （※1必須）	integer	JANコード検索、JANコードによって一意の商品のレビュー一覧を取得します。
        例：jan=4988601006200
        category_id
        （※1必須）	integer	カテゴリID、カテゴリIDによって指定したカテゴリの商品レビュー一覧を取得します。
        product_id
        （※1必須）	integer	Y!ショッピング製品コード廃止のため削除
        製品ID、製品IDによって一意の商品のレビュー一覧を取得します。
        例：product_id=e8c175ee5dee0f73dc7bd5026606d97a
        person_id
        （※1必須）	integer	人物コード、人物コードによって指定した人物に関連する商品のレビュー一覧を取得します。
        例：person_id=2640
        store_id
        （※1必須）	string	ストアID、ストアIDによって指定したストアの商品レビュー一覧を取得します。
        例：store_id=hmv
        results	integer	結果数指定、取得する検索結果数の指定　デフォルト値は10件、最大値は50件
        start	integer	オフセット、何件目から表示させるか（１件目は1）
        sort	updatetime/review_rate	並べ替え、updatetime(更新時間順）/review_rate(レビュー評価点順）
        （デフォルト：-updatetime）
        降順は-、昇順は%2B
        例：sort=-review_rate
        """
        if all(v is None for v in (jan, category_id, product_id, person_id, store_id)):
            raise ValueError(
                "One of jan, category_id, product_id, person_id, store_id must be specified."
            )
        return await self.fetch(
            "https://shopping.yahooapis.jp/ShoppingWebService/V1/json/reviewSearch",
            **{
                "appid": self.appid,
                "affiliate_type": affiliate_type,
                "affiliate_id": affiliate_id,
                "callback": callback,
                "jan": jan,
                "category_id": category_id,
                "product_id": product_id,
                "person_id": person_id,
                "store_id": store_id,
                "results": results,
                "start": start,
                "sort": sort,
            },
        )

    @cachedasyncmethod(cache=lambda self: self.cache)
    async def searchScrape(self, query: str) -> list[NestedDict]:
        async with self.session.get(
            "https://shopping.yahoo.co.jp/search", params={"p": query}
        ) as response:
            text = await response.text()
            cont = html.fromstring(text)
            scripts = cont.xpath("//script[contains(@type, 'json')]/text()")
            return [self.json_decoder.decode(script) for script in scripts]

    @cachedasyncmethod(cache=lambda self: self.cache)
    async def itemScrape(self, url: str) -> list[NestedDict]:
        results = []

        # intercept coupon request
        async def intercept_coupon() -> None:
            async with NetworkInterceptor(
                self.driver, patterns=[RequestPattern.AnyResponse]
            ) as interceptor:
                get_task = asyncio.create_task(self.driver.get(url, wait_load=False))
                async for data in interceptor:
                    print(data.request.url)
                    COUPON_URL = (
                        "https://store.shopping.yahoo.co.jp/syene-bff/v1/coupon/v2"
                    )
                    if isinstance(
                        data, InterceptedRequest
                    ) and data.request.url.startswith(COUPON_URL):
                        body = await data.body
                        if body is not None:
                            results.append(self.json_decoder.decode(body.decode()))
                        break
            await get_task  # no meaning

        # add timeout
        try:
            await asyncio.wait_for(intercept_coupon(), timeout=5)
        except asyncio.TimeoutError:
            warnings.warn(
                "Failed to intercept coupon request", RuntimeWarning, stacklevel=2
            )

        # extract json
        async with self.session.get(url) as response:
            text = await response.text()
            cont = html.fromstring(text)
            scripts = cont.xpath("//script[contains(@type, 'json')]/text()")
            return [self.json_decoder.decode(script) for script in scripts] + results

    async def itemPrice(self, url: str) -> ItemPrice:
        return ItemPrice.from_itemScrape(await self.itemScrape(url))
