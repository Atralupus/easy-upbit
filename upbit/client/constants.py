import enum


class CaptainCoin(enum.Enum):
    # 비트코인
    BTC = "BTC"


class MarketType(enum.Enum):
    # 비트코인 마켓
    BTC = "BTC"
    # 한화 마켓
    KRW = "KRW"
    # 이더리움 마켓
    ETH = "ETH"
    # 테더 마켓
    USDT = "USDT"
