from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, Depends,BackgroundTasks
from dotenv import load_dotenv
# from redis import RedisConnector

from app.decorators.custom_decorators import repeat_every
from app.football_sdk.api_client import FootballAPIClient
from app.core.telegram.telegram import TelegramHandler

# Loading enviromental variables from .env file
load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

@repeat_every(seconds=30)
async def send_message():
    prediction = await app.state.football_client.get_live_prediction_for_ongoing_match()
    await app.state.telegram_client.send_message(prediction)

# async def send_prediction_to_telegram(prediction):
    # await client.send_message(entity=group_entity,message=message)

async def get_telegram_client():
    client = TelegramHandler(api_id,api_hash)
    await client.start()
    try:
        return client
    except Exception as e:
        print(e)

@asynccontextmanager
async def lifespan(app: FastAPI, background_tasks: BackgroundTasks):
    app.state.telegram_client = await get_telegram_client()
    app.state.football_client = FootballAPIClient(api_key=os.getenv('RAPID_API_KEY')) 
    background_tasks.add_task(await send_message())
    yield

app = FastAPI(lifespan=lifespan,background_tasks)

@app.get("/test")
async def test():
    prediction = await app.state.football_client.get_live_prediction_for_ongoing_match()
    group_entity = await app.state.telegram_client.get_entity("t.me/BetSmartHub")
    await app.state.telegram_client.send_message(entity=group_entity,message=prediction)

@app.get("/predictions/{fixture_id}")
async def get_predictions_for_fixture(fixture_id: int):
    predictions = await app.state.football_client.get_predictions_for_fixture(fixture_id)
    return predictions

@app.get("/live")
async def get_live_fixtures():
    live_fixtures = await app.state.football_client.get_live_fixtures()
    return live_fixtures

@app.get('/get_pred')
async def get_pred():
    prediction = await app.state.football_client.get_prediction_for_fixture('test_id')
    return prediction

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000,reload=True)