import json

from aiohttp.web import Request
from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import SimpleCookieStorage, session_middleware

from app.web.models.application import Application
from app.web.utils import error_json_response

HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: Request, handler):
    try:
        response = await handler(request)
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=_error_txt(e),
        )
    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status],
            message=str(e.reason),
            data=None,
        )
    except Exception as e:
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500],
            message=str(e),
            data=None,
        )
    return response


def _error_txt(exception: HTTPException) -> dict | None:
    if exception.text:
        return json.loads(exception.text)
    return None


def setup_middlewares(app: Application):
    app.middlewares.append(session_middleware(SimpleCookieStorage()))
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
