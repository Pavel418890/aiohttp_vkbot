import asyncio
import typing
from datetime import datetime
from typing import Optional

import aiohttp
from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message, Update
from app.store.vk_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.poller: Optional[Poller] = None
        self.ts: Optional[int] = None

    async def connect(self, app: "Application"):
        self.session = aiohttp.ClientSession()
        await self._get_long_poll_service()
        self.poller = Poller(self.app.store)
        await self.poller.start()
        pass
    async def disconnect(self, app: "Application"):
        if self.session and not self.session.closed:
            await self.session.close()
        if self.poller and self.poller.is_running:
            await self.poller.stop()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        url = host + method + "?"
        if "v" not in params:
            params["v"] = "5.131"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def _get_long_poll_service(self):
        url = self._build_query(
            host="https://api.vk.com/",
            method="method/groups.getLongPollServer",
            params={
                "access_token": self.app.config.bot.token,
                "group_id": self.app.config.bot.group_id,
            }
        )
        async with self.session.get(url) as response:
            lps = await response.json()
            self.key = lps["response"]["key"]
            self.server = lps["response"]["server"]
            self.ts = lps["response"]["ts"]

    async def poll(self):
        url = self._build_query(
            host=self.server,
            method="",
            params={
                "act": "a_check",
                "key": self.key,
                "ts": self.ts,
                "wait": "25"
            }
        )
        async with self.session.get(url) as response:
            result = await response.json()
            self.ts = result["ts"]
            updates = [Update(**update) for update in result["updates"]]
            return updates

    async def send_message(self, message: Message) -> None:
        url = self._build_query(
            host="https://api.vk.com/",
            method="method/messages.send",
            params={
                "access_token": self.app.config.bot.token,
                "message": message.text,
                "peer_id": message.peer_id,
                "random_id": int(datetime.now().timestamp())

            }
        )
        async with self.session.post(url) as response:
            self.app.logger.info(await response.json())
