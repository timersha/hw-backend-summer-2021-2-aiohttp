from app.base.base_accessor import BaseAccessor
from app.quiz.models import Answer, Question, Theme


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = Theme(id=self.app.database.next_theme_id, title=title)
        self.app.database.themes.append(theme)
        return theme

    async def get_theme_by_title(self, title: str) -> Theme | None:
        for item in self.app.database.themes:
            if item.title == title:
                return item
        return None

    async def get_theme_by_id(self, id_: int) -> Theme | None:
        for item in self.app.database.themes:
            if item.id == id_:
                return item
        return None

    async def list_themes(self) -> list[Theme]:
        return self.app.database.themes

    async def get_question_by_title(self, title: str) -> Question | None:
        for item in self.app.database.questions:
            if item.title == title:
                return item
        return None

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        question = Question(
            id=self.app.database.next_question_id,
            title=title,
            theme_id=theme_id,
            answers=answers,
        )
        self.app.database.questions.append(question)
        return question

    async def list_questions(self, theme_id: int) -> list[Question]:
        if not theme_id:
            return self.app.database.questions
        list_questions: list[Question] = []
        for item in self.app.database.questions:
            if item.theme_id == theme_id:
                list_questions.append(item)
        return list_questions
