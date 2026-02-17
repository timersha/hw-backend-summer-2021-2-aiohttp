from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp_session import get_session

from app.web.models.request import Request


class AuthRequiredMixin:
    def __init__(self, request: Request) -> None:
        self._request = request

    @property
    def request(self) -> Request:
        return self._request

    async def is_auth(self) -> bool:
        session = await get_session(self.request)
        session_key = self.request.app.config.session.key
        request_session_key = session.get("session_key", None)
        if not request_session_key:
            raise HTTPUnauthorized()
        if request_session_key != session_key:
            raise HTTPForbidden()
        return True
