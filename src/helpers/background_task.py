import asyncio

from src.football_sdk.screenshot import screenshot_fixture

class BackgroundRunner:
    def __init__(self):
        self.value = 0

    async def send_message(self,app,seconds):
        while True:
            prediction , fixture_id = await app.state.football_client.get_live_prediction_for_ongoing_match()
            if fixture_id:
                path = await screenshot_fixture(fixture_id)
            await app.state.telegram_client.send_message_with_photo(prediction,path)
            # await telegram_client.send_message(prediction)
            await asyncio.sleep(seconds)