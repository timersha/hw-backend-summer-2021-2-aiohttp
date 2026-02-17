from collections.abc import Awaitable, Callable

from aiohttp.web import Application as AiohttpApplication

from app.store.database.database import Database
from app.store.store import Store
from app.web.config import Config


class Application(AiohttpApplication):
    config: Config
    store: Store
    database: Database = Database()

    def register_accessor(
        self, connect_fn: Callable[["Application"], Awaitable[None]]
    ):
        self.on_startup.append(lambda aioapp: connect_fn(self))

    def register_cleanup(
        self, disconnect_fn: Callable[["Application"], Awaitable[None]]
    ):
        self.on_cleanup.append(lambda aioapp: disconnect_fn(self))
