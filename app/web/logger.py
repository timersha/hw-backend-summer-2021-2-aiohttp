import logging

from app.web.models.application import Application


def setup_logging(_: Application) -> None:
    logging.basicConfig(level=logging.INFO)
