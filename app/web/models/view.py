from typing import cast

from aiohttp.web import View as AiohttpView

from app.store import Store
from app.web.models.request import Request


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return cast(Request, super().request)

    @property
    def store(self) -> Store:
        return cast(Store, self.request.app.store)

    @property
    def data(self) -> dict:
        return self.request.get("data", {})
