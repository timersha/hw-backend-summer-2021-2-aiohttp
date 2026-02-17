from typing import Any, cast

from aiohttp.web_exceptions import (
    HTTPBadRequest,
    HTTPConflict,
    HTTPNotFound,
    HTTPUnauthorized,
)
from aiohttp_apispec import request_schema

from app.quiz.models import Answer
from app.quiz.schemes import QuestionSchema
from app.web.mixins.AuthRequiredMixin import AuthRequiredMixin
from app.web.models.view import View
from app.web.utils import json_response


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    async def post(self):
        is_auth = await self.is_auth()
        if not is_auth:
            raise HTTPUnauthorized
        title = self.data["title"]
        theme_id = self.data["theme_id"]
        answers = []
        answers_data = self.data["answers"]
        quizzes = self.store.quizzes
        question_exist = await quizzes.get_question_by_title(title)
        theme_exist = await quizzes.get_theme_by_id(theme_id)
        is_true_count = 0
        if not theme_exist:
            raise HTTPNotFound
        if len(answers_data) < 2:
            raise HTTPBadRequest
        for item in answers_data:
            is_true_count += 1 if item["is_correct"] else 0
            answers.append(Answer(**item))
        if is_true_count != 1:
            raise HTTPBadRequest
        if question_exist:
            raise HTTPConflict
        question = await quizzes.create_question(
            title=title, theme_id=theme_id, answers=answers
        )
        question_dump = cast(dict[str, Any], QuestionSchema().dump(question))
        if not question_dump:
            raise HTTPNotFound
        return json_response(data=question_dump)
