import asyncio

from app.decorators.custom_decorators import repeat_every

class BackgroundRunner:
    def __init__(self):
        self.value = 0

    async def send_message(self,seconds,telegram_client,football_client):
        while True:
            prediction = await football_client.get_live_prediction_for_ongoing_match()
            await telegram_client.send_message(prediction)
            await asyncio.sleep(seconds)