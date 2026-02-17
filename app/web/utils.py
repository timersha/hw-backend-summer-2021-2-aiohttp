from hashlib import sha256

from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response


def get_password_hash(password: str) -> str:
    password_hash = sha256()
    password_hash.update(password.encode())
    return password_hash.hexdigest()


def json_response(data: dict | None = None, status: str = "ok") -> Response:
    if data is None:
        data = {}

    return aiohttp_json_response(
        data={
            "status": status,
            "data": data,
        }
    )


def error_json_response(
    http_status: int,
    status: str = "error",
    message: str | None = None,
    data: dict | None = None,
):
    if data is None:
        data = {}
    return aiohttp_json_response(
        status=http_status,
        data={
            "status": status,
            "message": message,
            "data": data,
        },
    )
