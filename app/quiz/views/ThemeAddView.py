from typing import Any, cast

from aiohttp.web_exceptions import (
    HTTPConflict,
    HTTPNotFound,
    HTTPUnauthorized,
)
from aiohttp_apispec import request_schema

from app.quiz.schemes import ThemeSchema
from app.web.mixins.AuthRequiredMixin import AuthRequiredMixin
from app.web.models.view import View
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    async def post(self):
        is_auth = await self.is_auth()
        if not is_auth:
            raise HTTPUnauthorized
        title = self.data["title"]
        theme_exist = await self.store.quizzes.get_theme_by_title(title)
        if theme_exist:
            raise HTTPConflict
        theme = await self.store.quizzes.create_theme(title=title)
        theme_dump = cast(dict[str, Any], ThemeSchema().dump(theme))
        if not theme_dump:
            raise HTTPNotFound
        return json_response(data=theme_dump)
