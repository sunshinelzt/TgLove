import logging
from asyncio import sleep
from typing import Union

import requests
from telethon.tl.types import Message

from .. import loader, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)

@loader.tds
class LoveMagic(loader.Module):
    """Animation of hearts without spamming logs and floodwaiters"""

strings = {
        "message": "<b>❤️‍🔥 Я хочу тебе сказать кое-что...</b>\n<i>{}</i>",
        "_cls_doc": "Анимация сердечек без спама в логи и флудвейтов",
    }

    async def client_ready(self):
        self.classic_frames = (
            await utils.run_sync(
                requests.get,
                "https://raw.githubusercontent.com/sunshinelzt/TgLove/main/ily_classic.json",
            )
        ).json()

    async def ily_handler(
        self,
        obj: Union[InlineCall, Message],
        text: str,
        inline: bool = False,
    ):
        frames = self.classic_frames + [
            f'<b>{" ".join(text.split()[: i + 1])}</b>'
            for i in range(len(text.split()))
        ]

        obj = await self.animate(obj, frames, interval=0.5, inline=inline)
        await obj.unload()

    @loader.command(ru_doc="Отправить анимацию сердец в инлайне")
    async def ilyicmd(self, message: Message):
        """Отправить сообщение с анимацией сердец в инлайне"""
        args = utils.get_args_raw(message)
        await self.inline.form(
            self.strings("message").format("*" * (len(args) or 9)),
            reply_markup={
                "text": "🧸 Открыть",
                "callback": self.ily_handler,
                "args": (args or "Я ❤️ тебя!",),
                "kwargs": {"inline": True},
            },
            message=message,
            disable_security=True,
        )

    @loader.command(ru_doc="Отправить анимацию сердец")
    async def ily(self, message: Message):
        """Отправить сообщение с анимацией сердец"""
        await self.ily_handler(
            message,
            utils.get_args_raw(message) or "Я ❤️ тебя!",
            inline=False,
        )
