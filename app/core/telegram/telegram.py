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

    async def send_message(self, prediction):
        """
        Send a message to a chat
        :param chat_id: chat id
        :param text: message text
        :return: None
        """
        async with self.client:
            channel_entity = await self.client.get_entity("t.me/BetSmartHub")
            await self.client.send_message(entity=channel_entity,message=prediction)