import asyncio
import os
import emoji

from src.football_sdk.screenshot import screenshot_fixture

class BackgroundRunner:
    def __init__(self):
        self.value = 0

    async def send_message(self,seconds,football_client,telegram_client):
        while True:
            prediction , fixture_id = await football_client.get_live_prediction_for_ongoing_match()
            # prediction = 'test'
            # fixture_id = 1037532
            # Found fixture to post
            emojis_before = emoji.emojize('🔥🔥 Live Bet\n💯')
            emojis_after = emoji.emojize('\n ✅✅✅✅✅✅')

            caption = ''.join([emojis_before,prediction,emojis_after])
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