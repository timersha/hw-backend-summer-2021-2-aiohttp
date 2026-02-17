from app.admin.views import AdminCurrentView, AdminLoginView
from app.web.models.application import Application


def setup_routes(app: Application):
    app.router.add_view("/admin.login", AdminLoginView)
    app.router.add_view("/admin.current", AdminCurrentView)
