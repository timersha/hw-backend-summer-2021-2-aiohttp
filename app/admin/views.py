from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminSchemaIn
from app.web.mixins.AuthRequiredMixin import AuthRequiredMixin
from app.web.models.view import View

from .schemes import AdminSchemaOut


class AdminLoginView(AuthRequiredMixin, View):
    @request_schema(AdminSchemaIn)
    async def post(self):
        data = self.request["data"]
        email = data["email"]
        password = data["password"]
        admin = await self.store.admins.login(email=email, password=password)
        if not admin:
            raise HTTPForbidden
        session_id = self.store.admins.app.config.session.key
        session = await new_session(request=self.request)
        session["session_key"] = session_id
        data = AdminSchemaOut().dump(admin)
        return json_response(data={"status": "ok", "data": data})


class AdminCurrentView(AuthRequiredMixin, View):
    async def get(self):
        is_auth = await self.is_auth()
        if not is_auth:
            raise HTTPUnauthorized
        email = self.store.admins.app.config.admin.email
        admin = await self.store.admins.get_by_email(email=email)
        data = AdminSchemaOut().dump(admin)
        return json_response(data={"status": "ok", "data": data})
