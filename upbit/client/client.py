import datetime
import functools
import json
import typing

import requests
from requests_toolbelt.sessions import BaseUrlSession

from .data import Coin, MinuteCandle
from .exc import UpbitClientResponseError

MAX_RETRY_COUNT = 3


class UpbitClient(object):
    def __init__(self, proxy: typing.Optional[str] = None):
        super().__init__()

        self.session = BaseUrlSession("https://api.upbit.com/")

        if proxy:
            self.session.proxies.update(
                {
                    "http": f"http://{proxy}",
                    "https": f"https://{proxy}",
                }
            )

    def request_retryer(self, request: typing.Callable):
        retry_count = 0

        while retry_count <= MAX_RETRY_COUNT:
            try:
                return request()
            except requests.exceptions.ConnectionError as e:
                retry_count += 1

                if retry_count == MAX_RETRY_COUNT:
                    raise e

    def _handle_response(self, response: requests.Response) -> typing.Any:
        text_value = response.text

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise UpbitClientResponseError(response.status_code, text_value)

        try:
            value = response.json()

            if not value:
                raise UpbitClientResponseError(
                    response.status_code, text_value
                )

        except json.JSONDecodeError:
            raise UpbitClientResponseError(response.status_code, text_value)

        return value

    def fetch_coin_list(self) -> typing.List[Coin]:
        params = {"isDetails": True}

        request = functools.partial(
            self.session.get,
            "/v1/market/all",
            params=params,
            **self.default_request_params,
        )

        response = self._handle_response(self.retryer.run(request))

        return [Coin.from_json(x) for x in response]

    def fetch_price_candles_minute(
        self,
        coin: Coin,
        minute: typing.Literal[1, 3, 5, 15, 10, 30, 60, 240],
        *,
        last_candle_datetime: typing.Optional[datetime.datetime] = None,
        candle_count: typing.Optional[int] = None,
    ) -> typing.List[MinuteCandle]:
        params = {
            "market": coin.market_code,
            "count": candle_count,
            "to": last_candle_datetime,
        }

        request = functools.partial(
            self.session.get,
            f"/v1/candles/minutes/{minute}",
            params=params,
            **self.default_request_params,
        )

        response = self._handle_response(self.retryer.run(request))

        return [MinuteCandle.from_json(x) for x in response]
