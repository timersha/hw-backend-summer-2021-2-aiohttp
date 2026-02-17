from logging import getLogger

from app.web.models.application import Application


class BaseAccessor:
    def __init__(self, app: Application, *args, **kwargs):
        self.app = app
        self.logger = getLogger("accessor")
        app.register_accessor(self.connect)
        app.register_cleanup(self.disconnect)

    async def connect(self, app: Application):
        return

    async def disconnect(self, app: Application):
        return
