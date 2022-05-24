import json
import typing

import aiohttp_session
from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPException
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware

from app.admin.models import Admin
from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request

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
async def is_authenticated_middleware(request: "Request", handler):
    session = await aiohttp_session.get_session(request)
    existing_admin = session.get("admin", None)
    if existing_admin:
        request.admin = Admin(
            id=existing_admin["id"],
            email=existing_admin["email"]
        )
    else:
        request.admin = None
    return await handler(request)


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status] or HTTP_ERROR_CODES[400],
            message=e.reason,
            data=e.text
        )
    except Exception as e:
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500],
            message=str(e)
        )


def setup_middlewares(app: "Application"):
    app.middlewares.append(is_authenticated_middleware)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
