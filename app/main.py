from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from dotenv import load_dotenv

from decorators.custom_decorators import repeat_every
from football_sdk.api_client import FootballAPIClient

# Loading enviromental variables from .env file
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print_test()
    yield

app = FastAPI(lifespan=lifespan)

@repeat_every(seconds=30000) 
def print_test() -> None:
    print('test')

app = FastAPI()
api_client = FootballAPIClient(api_key=os.getenv('RAPID_API_KEY'))


@app.get("/predictions/{fixture_id}")
async def get_predictions_for_fixture(fixture_id: int):
    predictions = await api_client.get_predictions_for_fixture(fixture_id)
    return predictions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)