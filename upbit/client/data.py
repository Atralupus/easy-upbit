import datetime
import decimal

import attr
import typing

from .constants import MarketType


@attr.s(frozen=True, auto_attribs=True)
class CoinSpec(object):
    # data: MarketType
    # description: 거래가능한 마켓
    market: MarketType
    # data: BTC
    # description: 코인 약자
    name: str
    # data: 비트코인
    # description: 코인 한글명칭
    korean_name: str
    # data: 비트코인
    # description: 코인 영문명칭
    english_name: str


@attr.s(frozen=True, auto_attribs=True)
class BaseCandleResponse(object):
    # data: MarketType
    # description: 거래가능한 마켓
    market: MarketType
    # data: BTC
    # description: 코인 약자
    name: str
    # data: 2021-02-16T04:21:00
    # description: 캔들 기준 시각(UTC 기준)
    candle_date_time_utc: datetime.datetime
    # data: 2021-02-16T13:21:00
    # description: 캔들 기준 시각(KST 기준)
    candle_date_time_kst: datetime.datetime
    # data: 0.03667325
    # description: 시가
    opening_price: decimal.Decimal
    # data: 0.03667325
    # description: 고가
    high_price: decimal.Decimal
    # data: 0.03667325
    # description: 저가
    low_price: decimal.Decimal
    # data: 0.03667325
    # description: 종가
    trade_price: decimal.Decimal
    # data: 1613449283458
    # description: 해당 캔들에서 마지막 틱이 저장된 시각
    timestamp: float
    # data: 0.00526974
    # description: 누적 거래 금액
    candle_acc_trade_price: decimal.Decimal
    # data: 0.14369452
    # description: 누적 거래량
    candle_acc_trade_volume: decimal.Decimal


def market_splitter(value: str) -> typing.Tuple[MarketType, str]:
    temp = value.split("-")

    return MarketType(temp[0]), temp[1]


class UpbitData(object):
    pass


@attr.s(frozen=True, auto_attribs=True)
class Coin(UpbitData, CoinSpec):
    # data: False
    # description: 유의 종목 여부{NONE (해당 사항 없음), CAUTION(투자유의)}
    market_warning: bool
    #: Raw JSON data
    raw_data: typing.Dict[str, typing.Any] = attr.ib(repr=False)

    @classmethod
    def from_json(cls, data: typing.Dict[str, typing.Any]) -> "Coin":
        market_warning = data.get("market_warning") == "CAUTION"
        market, name = market_splitter(data["market"])

        return cls(
            market=market,
            name=name,
            korean_name=data["korean_name"],
            english_name=data["english_name"],
            market_warning=market_warning,
            raw_data=data,
        )

    @property
    def market_code(self):
        return f"{self.market.value}-{self.name}"


@attr.s(frozen=True, auto_attribs=True)
class MinuteCandle(BaseCandleResponse):
    # data: 1
    # description: 분 단위(유닛)
    unit: int
    #: Raw JSON data
    raw_data: typing.Dict[str, typing.Any] = attr.ib(repr=False)

    @classmethod
    def from_json(cls, data: typing.Dict[str, typing.Any]) -> "MinuteCandle":
        market, name = market_splitter(data["market"])

        return cls(
            market=market,
            name=name,
            candle_date_time_utc=datetime.datetime.fromisoformat(
                data["candle_date_time_utc"]
            ),
            candle_date_time_kst=datetime.datetime.fromisoformat(
                data["candle_date_time_kst"]
            ),
            opening_price=decimal.Decimal(data["opening_price"]),
            high_price=decimal.Decimal(data["high_price"]),
            low_price=decimal.Decimal(data["low_price"]),
            trade_price=decimal.Decimal(data["trade_price"]),
            timestamp=float(data["timestamp"]),
            candle_acc_trade_price=decimal.Decimal(
                data["candle_acc_trade_price"]
            ),
            candle_acc_trade_volume=decimal.Decimal(
                data["candle_acc_trade_volume"]
            ),
            unit=int(data["unit"]),
            raw_data=data,
        )
