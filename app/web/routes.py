from app.admin.routes import setup_routes as admin_setup_routes
from app.quiz.routes import setup_routes as quiz_setup_routes
from app.web.models.application import Application


def setup_routes(app: Application):
    admin_setup_routes(app)
    quiz_setup_routes(app)
