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
        # Crete session directory if does not exist
        session_directory = os.path.join(os.getcwd(), 'app\\core\\telegram\\session')
        if not os.path.isdir(session_directory):
            os.makedirs(session_directory)
        self.session_id = session_directory + '\\bot_session'
    
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