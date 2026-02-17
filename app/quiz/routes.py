from app.quiz.views.QuestionAddView import QuestionAddView
from app.quiz.views.QuestionListView import QuestionListView
from app.quiz.views.ThemeAddView import ThemeAddView
from app.quiz.views.ThemeListView import ThemeListView
from app.web.models.application import Application


def setup_routes(app: Application):
    app.router.add_view("/quiz.add_theme", ThemeAddView)
    app.router.add_view("/quiz.list_themes", ThemeListView)
    app.router.add_view("/quiz.add_question", QuestionAddView)
    app.router.add_view("/quiz.list_questions", QuestionListView)
