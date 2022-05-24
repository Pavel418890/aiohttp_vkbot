import aiohttp_session
from aiohttp.web_response import StreamResponse
from aiohttp.web_exceptions import HTTPUnauthorized


class AuthRequiredMixin:
    async def _iter(self) -> StreamResponse:
        if not self.request.admin:
            raise HTTPUnauthorized
        return await super()._iter()
