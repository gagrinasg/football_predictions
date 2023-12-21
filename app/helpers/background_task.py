import asyncio
import os
import logging

from app.football_sdk.screenshot import screenshot_fixture
from app.core.llms.llm_handler import LLMHandler

class BackgroundRunner:
    def __init__(self):
        self.value = 0
        self.llm_handler = LLMHandler()

    async def send_message(self,seconds,football_client,telegram_client):
        while True:
            try:
                prediction , fixture_id = await football_client.get_live_prediction_for_ongoing_match()

                ai_response = await self.llm_handler._create_message(prediction)
                caption = ai_response.content
                if fixture_id:
                    screenshot_path = await screenshot_fixture(fixture_id)
                    await telegram_client.send_message_with_photo(caption,screenshot_path)
                    # await telegram_client.send_message(prediction)

                    # Delete the screenshot
                    if os.path.exists(screenshot_path):
                        os.remove(screenshot_path)
                else:
                    # No fixture found
                    # Set timeout to 1 minute to poll more frequently 
                    seconds = 60

                await asyncio.sleep(seconds)
            except Exception as e:
                logging.error(e)
