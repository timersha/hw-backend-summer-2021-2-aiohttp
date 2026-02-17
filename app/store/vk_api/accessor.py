import random
from urllib.parse import urlencode, urljoin

from aiohttp.client import ClientResponse, ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import (
    Message,
    Update,
    UpdateMessage,
    UpdateObject,
)
from app.store.vk_api.poller import Poller
from app.web.models.application import Application

API_VERSION = "5.131"


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: Application, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: ClientSession | None = None
        self.key: str | None = None
        self.server: str | None = None
        self.poller: Poller | None = None
        self.ts: int | None = None

    async def poll(self):
        if not self.session or not self.server:
            return
        if not self.session.closed:
            params = {
                "act": "a_check",
                "key": self.key,
                "ts": self.ts,
                "wait": 1,
            }
            url = self._build_query(self.server, "", params)
            response = await self.session.get(url)
            if response.ok:
                data = await response.json()
                self.ts = data.get("ts")
                updates = []
                updates_data = data.get("updates")
                for update_data in updates_data:
                    message_data = update_data["object"]["message"]
                    update_type = update_data["type"]
                    id_ = message_data["id"]
                    from_id = message_data["from_id"]
                    text = message_data["text"]
                    message = UpdateMessage(from_id, text, id_)
                    update_object = UpdateObject(message)
                    update = Update(update_type, update_object)
                    updates.append(update)
                await self.app.store.bots_manager.handle_updates(updates)

    async def send_message(self, message: Message) -> None:
        if not self.session:
            return
        params = {
            "access_token": self.access_token,
            "random_id": random.randint(1, 1000000),
            "message": message.text,
            "chat_id": 3,
        }
        url = self._build_query(
            "https://api.vk.com/", "method/messages.send", params
        )
        await self.session.get(url)

    async def connect(self, app: Application):
        self.access_token = app.config.bot.token
        self.group_id = app.config.bot.group_id
        params = {"group_id": self.group_id, "access_token": self.access_token}
        url = self._build_query(
            "https://api.vk.com/", "method/groups.getLongPollServer", params
        )
        client_session = ClientSession()
        response = await client_session.get(url)
        if response.ok:
            await self._handle_response(response, client_session, app)

    async def disconnect(self, app: Application):
        if not self.session or not self.poller:
            return
        if not self.session.closed:
            await self.session.close()
        await self.poller.stop()

    async def _handle_response(
        self,
        response: ClientResponse,
        client_session: ClientSession,
        app: Application,
    ):
        data = await response.json()
        data_response = data.get("response")
        self.session = client_session
        self.key = data_response.get("key")
        self.server = data_response.get("server")
        self.ts = data_response.get("ts")
        self.poller = Poller(app.store)
        await self.poller.start()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        params.setdefault("v", API_VERSION)
        return f"{urljoin(host, method)}?{urlencode(params)}"

    async def _get_long_poll_service(self):
        raise NotImplementedError
