####--------------------------------####
#--# Name:     TgLove               #--#
#--# Author:   by sunshine          #--#
####--------------------------------####

import logging
from typing import Union

import requests
from telethon.tl.types import Message

from .. import loader, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TgLove(loader.Module):
    """Animation of hearts without spamming logs and floodwaiters"""

    strings = {
        "message": "<b>❤️‍🔥 Я хочу тебе сказать кое-что...</b>\n<i>{}</i>",
        "_cls_doc": "Анимация сердечек без спама в логи и флудвейтов",
    }

    def __init__(self):
        super().__init__()
        self.classic_frames = []

    async def client_ready(self):
        try:
            response = await utils.run_sync(
                requests.get,
                "https://raw.githubusercontent.com/sunshinelzt/TgLove/main/ily_classic.json",
            )
            response.raise_for_status()
            self.classic_frames = response.json()
        except (requests.RequestException, ValueError) as e:
            logger.error(f"Failed to fetch classic frames: {e}")

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

        try:
            obj = await self.animate(obj, frames, interval=0.5, inline=inline)
        except Exception as e:
            logger.error(f"Animation failed: {e}")

    @loader.command(ru_doc="Отправить анимацию сердец в инлайне")
    async def ilyicmd(self, message: Message):
        """Отправить сообщение с анимацией сердец в инлайне"""
        args = utils.get_args_raw(message)
        try:
            await self.inline.form(
                self.strings["message"].format("*" * (len(args) or 9)),
                reply_markup={
                    "text": "🧸 Открыть",
                    "callback": self.ily_handler,
                    "args": (args or "Я люблю тебя!",),
                    "kwargs": {"inline": True},
                },
                message=message,
                disable_security=True,
            )
        except Exception as e:
            logger.error(f"Inline form submission failed: {e}")

    @loader.command(ru_doc="Отправить анимацию сердец")
    async def ily(self, message: Message):
        """Отправить сообщение с анимацией сердец"""
        try:
            await self.ily_handler(
                message,
                utils.get_args_raw(message) or "Я люблю тебя!",
                inline=False,
            )
        except Exception as e:
            logger.error(f"Sending animation failed: {e}")
