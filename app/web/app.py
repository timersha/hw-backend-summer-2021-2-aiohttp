from aiohttp_apispec import setup_aiohttp_apispec

from app.store.store import setup_store
from app.web.config import setup_config
from app.web.logger import setup_logging
from app.web.middlewares import setup_middlewares
from app.web.models.application import Application
from app.web.routes import setup_routes


def setup_app(config_path: str) -> Application:
    app = Application()
    setup_logging(app)
    setup_config(app, config_path)
    setup_routes(app)
    setup_aiohttp_apispec(
        app, title="Application", url="/openapi/json", swagger_path="/openapi"
    )
    setup_middlewares(app)
    setup_store(app)
    return app
