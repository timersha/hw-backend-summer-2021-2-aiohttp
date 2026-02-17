from app.admin.models import Admin
from app.base.base_accessor import BaseAccessor
from app.web.models.application import Application
from app.web.utils import get_password_hash


class AdminAccessor(BaseAccessor):
    async def connect(self, app: Application) -> None:
        email = self.app.config.admin.email
        password = get_password_hash(self.app.config.admin.password)
        await self.create_admin(email=email, password=password)

    async def get_by_email(self, email: str) -> Admin | None:
        for item in self.app.database.admins:
            if item.email == email:
                return item
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        # TODO: Обработать кейс когда email уже занят
        admin = await self.get_by_email(email)
        if not admin:
            id_ = len(self.app.database.admins) + 1
            admin = Admin(
                id=id_,
                email=email,
                password=password,
            )
            self.app.database.admins.append(admin)
        return admin

    async def login(self, email: str, password: str) -> Admin | None:
        # TODO: Выглядит так что логика проверки пароля не должна быть тут
        admin = await self.get_by_email(email)
        if not admin:
            return None
        password_hash = get_password_hash(password)
        if password_hash == admin.password:
            return admin
        return None
