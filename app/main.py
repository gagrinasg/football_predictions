from contextlib import asynccontextmanager
import os
import asyncio
import logging

from fastapi import FastAPI, BackgroundTasks,Depends
from dotenv import load_dotenv
from aiocron import crontab
import uvicorn


from decorators.custom_decorators import repeat_every
from football_sdk.api_client import FootballAPIClient
from core.telegram import TelegramHandler

# Loading enviromental variables from .env file
load_dotenv()

# @repeat_every(seconds=1) 
# async def background_task() -> None:
#     await telegram_handler.send_message()

# @asynccontextmanager
# async def lifespan(app: FastAPI,background_tasks: BackgroundTasks):
#     background_tasks.add_task(crontab("* * * * *").every(1), background_task)
#     yield
#     print("Shutting down FASTSSSSS")

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = TelegramHandler(api_id,api_hash)
    print('it goes na na na')
    await client.connect()
    yield

app = FastAPI(lifespan=lifespan)

app = FastAPI()
api_client = FootballAPIClient(api_key=os.getenv('RAPID_API_KEY'))

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

# telegram_handler = TelegramHandler(api_id,api_hash)

# Dependency to get or create the TelegramClient instance
# async def get_telegram_client():
#     if not hasattr(get_telegram_client, "_client"):
#         api_id = os.getenv('TELEGRAM_API_ID')
#         api_hash = os.getenv('TELEGRAM_API_HASH')
#         session_name = 'session_name'

#         client = TelegramClient(session_name, api_id, api_hash)

#         async with client:
#         # Await the connect method
#             await client.connect()
#             # message = await client.send_message(
#             # 'me',
#             # 'a [nice website](https://example.com)!',
#             # link_preview=False
#             # )
#             get_telegram_client._client = client

#     return get_telegram_client._client

# @app.get("/test")
# async def read_root(client: TelegramClient = Depends(get_telegram_client)):
#     # Now you can use the `client` instance in your route handler
#     # Do something with the client, e.g., client.send_message(...)
#     # api_id = int(os.getenv('TELEGRAM_API_ID'))
#     # api_hash = os.getenv('TELEGRAM_API_HASH')
#     # session_name = 'session_name'

#     # client = TelegramClient(session_name, api_id, api_hash)
#     # async with client:
#     #     await client.connect()
#     #     me = await client.get_me()
#     # return {"message": "Hello, FastAPI!"}
#     async with client:
#         me = await client.get_me()
#         # me.stringify()
#         channel_entity = await client.get_entity("https://t.me/+uA1XW4x1B1c0YWFk")
#         await client.send_message(entity=channel_entity,message='Hello, Telegram!')
#         return {"message": f"{me.stringify()}"}

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

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)