class UpbitClientError(Exception):
    """
    client 에러들입니다.
    """

    pass


class UpbitClientResponseError(UpbitClientError):
    """
    원하지 않은 response에 대한 에러입니다
    ex) json이 와야하는데 text가 왔을 경우, 404에러
    """

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(status_code, message)
