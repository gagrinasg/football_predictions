import os
import datetime

from telethon import TelegramClient, events, sync

class TelegramHandler():
    def __init__(self, api_id,api_hash):
        # Make sure to pass the required arguments to the superclass's __init__ method
        self.api_hash = api_hash
        self.api_id = api_id
    
    async def get_telegram_client(self):
        if not hasattr(self, "_client"):
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            session_name = f'bot_session_{timestamp}'

            client = TelegramClient(session_name, self.api_id, self.api_hash)

            async with client:
                # Await the connect method
                await client.connect()

                # You can perform additional initialization steps here if needed

                self._client = client

        return self._client

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

