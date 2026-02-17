from typing import cast

from aiohttp.web import Request as AiohttpRequest

from app.admin.models import Admin
from app.web.models.application import Application


class Request(AiohttpRequest):
    admin: Admin | None = None

    @property
    def app(self) -> Application:
        return cast(Application, super().app())
