from typing import Any, cast

from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized

from app.quiz.schemes import ThemeListSchema
from app.web.mixins.AuthRequiredMixin import AuthRequiredMixin
from app.web.models.view import View
from app.web.utils import json_response


class ThemeListView(AuthRequiredMixin, View):
    async def get(self):
        is_auth = await self.is_auth()
        if not is_auth:
            raise HTTPUnauthorized
        quizzes = self.store.quizzes
        themes = {"themes": await quizzes.list_themes()}
        theme_dump = cast(dict[str, Any], ThemeListSchema().dump(themes))
        if not theme_dump:
            raise HTTPNotFound
        return json_response(data=theme_dump)
