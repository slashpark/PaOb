from telegram import Bot
from telegram.error import TelegramError
import asyncio

class TelegramConnector:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id

    async def send_message_async(self, message: str) -> bool:
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode="HTML")
            return True
        except TelegramError as e:
            print(f"[TelegramConnector] Errore Telegram: {e}")
            return False

    def send_message(self, message: str) -> bool:
        return asyncio.run(self.send_message_async(message))
