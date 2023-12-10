import os
import datetime

from telethon import TelegramClient, events, sync
from telethon.sessions import StringSession

from decorators.custom_decorators import repeat_every

class TelegramHandler():
    def __init__(self, api_id,api_hash):
        # Make sure to pass the required arguments to the superclass's __init__ method
        self.api_hash = api_hash
        self.api_id = api_id
        # timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        # self.session_id = f'bot_session'
        # self.session_id = 'C:\\Users\\George\\Desktop\\Programming\\Projects\\draft polling\\bot_session'
        self.session_id = r'C:/Users/George/Desktop/Programming/Projects\draft_polling\app\core\telegram\session\bot_session'
    
    async def start(self):
        self.client = TelegramClient(self.session_id, self.api_id, self.api_hash)
        await self.client.start()
        # self.client.session.save()

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