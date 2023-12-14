import asyncio

from app.decorators.custom_decorators import repeat_every

from app.football_sdk.screenshot import screenshot_fixture

class BackgroundRunner:
    def __init__(self):
        self.value = 0

    async def send_message(self,seconds,telegram_client,football_client):
        while True:
            prediction , fixture_id = await football_client.get_live_prediction_for_ongoing_match()
            # prediction = 'test'
            # fixture_id = 718243
            if fixture_id:
                path = await screenshot_fixture(fixture_id)
            await telegram_client.send_message_with_photo(prediction,path)
            # await telegram_client.send_message(prediction)
            await asyncio.sleep(seconds)