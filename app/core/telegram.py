import os
import datetime

from telethon import TelegramClient, events, sync

from decorators.custom_decorators import repeat_every

class TelegramHandler():
    def __init__(self, api_id,api_hash):
        # Make sure to pass the required arguments to the superclass's __init__ method
        self.api_hash = api_hash
        self.api_id = api_id
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.session_id = f'bot_session_{timestamp}'
    
    async def start(self):
        self.client = TelegramClient(self.session_id, self.api_id, self.api_hash)
        await self.client.start()

    @staticmethod
    async def send_message(self, chat_id, text):
        """
        Send a message to a chat
        :param chat_id: chat id
        :param text: message text
        :return: None
        """
        async with self._client:
            group_entity = await self._client.get_entity("https://t.me/+uA1XW4x1B1c0YWFk")
            await self._client.send_message(entity=group_entity,message='Hello, Telegram!')