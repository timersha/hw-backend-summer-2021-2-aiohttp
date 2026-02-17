from typing import Any, cast

from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized
from aiohttp_apispec import querystring_schema

from app.quiz.schemes import ListQuestionSchema, ThemeIdSchema
from app.web.mixins.AuthRequiredMixin import AuthRequiredMixin
from app.web.models.view import View
from app.web.utils import json_response


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    async def get(self):
        is_auth = await self.is_auth()
        if not is_auth:
            raise HTTPUnauthorized
        quizzes = self.store.quizzes
        query_params = self.request["querystring"]
        theme_id = query_params.get("theme_id", None)
        questions = {"questions": await quizzes.list_questions(theme_id)}
        questions_dump = cast(
            dict[str, Any], ListQuestionSchema().dump(questions)
        )
        if not questions_dump:
            raise HTTPNotFound
        return json_response(data=questions_dump)
