from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from dotenv import load_dotenv

from decorators.custom_decorators import repeat_every
from football_sdk.api_client import FootballAPIClient
from core.telegram import TelegramHandler

from telethon.sessions import StringSession
from telethon import TelegramClient, events, sync

# Loading enviromental variables from .env file
load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')


@repeat_every(seconds=2)
async def send_message(client):
    async with client:
        await client.connect()
        message = 'Hello, Telegram!'
        group_entity = await client.get_entity("t.me/BetSmartHub")
        await client.send_message(entity=group_entity,message=message)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    client = TelegramClient('session_id',api_id,api_hash)
    await send_message(client)
    yield

app = FastAPI(lifespan=lifespan)

@repeat_every(seconds=1) 
def print_test() -> None:
    print('test')

api_client = FootballAPIClient(api_key=os.getenv('RAPID_API_KEY'))


@app.get("/predictions/{fixture_id}")
async def get_predictions_for_fixture(fixture_id: int):
    predictions = await api_client.get_predictions_for_fixture(fixture_id)
    return predictions

@app.get("/live")
async def get_live_fixtures():
    live_fixtures = await api_client.get_live_fixtures()
    return live_fixtures

@app.get('/get_pred')
async def get_pred():
    prediction = await api_client.get_prediction_for_fixture('test_id')
    return prediction

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000,reload=True)