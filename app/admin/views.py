from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp.web_response import Response
from aiohttp_apispec import response_schema, request_schema, docs
import aiohttp_session

from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response

from app.admin.schemes import AdminResponseSchema, AdminRequestSchema
from app.web.app import View


class AdminLoginView(View):

    @docs(
        tags=["admin"],
        summary="Authenticate method for admin",
        description="Check admin by provided credentials"
    )
    @request_schema(AdminRequestSchema)
    @response_schema(AdminResponseSchema, 200)
    async def post(self) -> Response:
        email = self.data["email"]
        password = self.data["password"]
        admin = await self.store.admins.get_by_email(email)
        if not admin:
            raise HTTPForbidden
        elif not admin.check_password(password):
            raise HTTPForbidden
        else:
            admin_data = AdminResponseSchema().dump(admin)
            session = await aiohttp_session.new_session(self.request)
            session["admin"] = admin_data
            return json_response(data=admin_data)


class AdminCurrentView(AuthRequiredMixin, View):

    @docs(
        tags=["admin"],
        summary="Return current admin",
        description="Check cookie storage/parse and try to find admin in db"
    )
    @response_schema(AdminResponseSchema, 200)
    async def get(self) -> Response:
        if not self.request.admin:
            raise HTTPUnauthorized
        return json_response(
            data=AdminResponseSchema().dump(self.request.admin)
        )
