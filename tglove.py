####--------------------------------####
#--# Name:     TgLove               #--#
#--# Author:   by sunshine          #--#
####--------------------------------####

import asyncio
import contextlib
import logging
import re
from datetime import datetime

from hikkatl.tl.functions.messages import StartBotRequest
from hikkatl.tl.types import Message

from .. import loader, utils

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

###########################
## Console color print
red    = [206, 76,  54]
green  = [68,  250, 123]
blue   = [253, 127, 233]
yellow = [241, 250, 118]
orange = [255, 184, 107]

def colored(color, text):
    """Returns a text string wrapped in ANSI escape codes for the specified color."""
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(color[0], color[1], color[2], text)

@loader.tds
class CustomModule(loader.Module):
    """Script for beautiful text layout"""

    strings = {
        "name": "TgLove",
        "ping": "pong",
        "error_t": "[" + colored(red, "Error") + "] " + "Не удалось выполнить команду [.t] Возможно был словлен flood.",
        "error_heart": "[" + colored(red, "Error") + "] " + "Не удалось выполнить команду [.heart] Возможно был словлен flood."
    }

    @loader.owner
    async def pingcmd(self, message):
        """Ответ на команду .ping"""
        try:
            await message.respond(self.strings("ping"))
            await asyncio.sleep(1)
            await message.delete()
        except Exception as e:
            logger.error(f"Error in pingcmd: {e}")

    @loader.owner
    async def tcmd(self, message):
        """Моделирование набора текста: .t <text>"""
        try:
            text = utils.get_args_raw(message)
            if not text:
                return
            orig_text = text
            tbp = ""  # to be printed
            typing_symbol = "/"
            while tbp != orig_text:
                typing_symbol = "_"
                await utils.edit_message(message, tbp + typing_symbol)
                await asyncio.sleep(0.1)
                tbp = tbp + text[0]
                text = text[1:]
                typing_symbol = "-"
                await utils.edit_message(message, tbp)
                await asyncio.sleep(0.1)
        except Exception as e:
            await message.respond(self.strings("error_t"))
            logger.error(f"Error in tcmd: {e}")

    @loader.owner
    async def heartcmd(self, message):
        """Анимация сердца: .heart <text>"""
        try:
            text = utils.get_args_raw(message) or "Создано с любовью by sunshine"
            heart_emoji = [
                "✨-💎",
                "✨-🌺",
                "☁️-😘",
                "✨-🌸",
                "🌾-🐸",
                "🔫-💥",
                "☁️-💟",
                "🍀-💖",
                "🌴-🐼",
            ]
            edit_heart = '''
            1 2 2 1 2 2 1
            2 2 2 2 2 2 2
            2 2 2 2 2 2 2
            1 2 2 2 2 2 1
            1 1 2 2 2 1 1
             1 1 1 2 1 1
            '''
            frame_index = 0
            while frame_index != len(heart_emoji):
                await utils.edit_message(message, edit_heart.replace("1", heart_emoji[frame_index].split("-")[0]).replace("2", heart_emoji[frame_index].split("-")[1]))
                await asyncio.sleep(1)
                frame_index += 1
            await utils.edit_message(message, text)
        except Exception as e:
            await message.respond(self.strings("error_heart"))
            logger.error(f"Error in heartcmd: {e}")