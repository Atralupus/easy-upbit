from requests import Session
from requests.adapters import HTTPAdapter


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 5
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def update_proxy(session: Session, proxy: str):
    session.proxies.update(
        {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}",
        }
    )
