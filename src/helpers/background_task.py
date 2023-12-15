import asyncio
import os

from src.football_sdk.screenshot import screenshot_fixture

class BackgroundRunner:
    def __init__(self):
        self.value = 0

    async def send_message(self,seconds,football_client,telegram_client):
        while True:
            prediction , fixture_id = await football_client.get_live_prediction_for_ongoing_match()
            if fixture_id:
                screenshot_path = await screenshot_fixture(fixture_id)
            await telegram_client.send_message_with_photo(prediction,screenshot_path)
            # await telegram_client.send_message(prediction)

            # Delete the screenshot
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)

            await asyncio.sleep(seconds)