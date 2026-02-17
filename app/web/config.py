import typing
from dataclasses import dataclass

import yaml

if typing.TYPE_CHECKING:
    from app.web.models.application import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class BotConfig:
    token: str
    group_id: str


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig
    bot: BotConfig


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    app.config = Config(
        admin=AdminConfig(
            email=config["admin"]["email"],
            password=config["admin"]["password"],
        ),
        bot=BotConfig(
            token=config["bot"]["token"],
            group_id=config["bot"]["group_id"],
        ),
        session=SessionConfig(
            key=config["session"]["key"],
        ),
    )
