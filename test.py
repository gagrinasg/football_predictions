from fastapi import FastAPI

# from fastapi_utils.tasks import repeat_every

from contextlib import asynccontextmanager
from decorators import repeat_every

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('test')
    print_test()
    yield
    print('after')

app = FastAPI(lifespan=lifespan)

@repeat_every(seconds=20)  # 1 hour
def print_test() -> None:
    # with sessionmaker.context_session() as db:
    #     remove_expired_tokens(db=db)
    print('test')

@app.get("/predict")
async def predict(x: float):
    return {}

if __name__ == "__main__":
    # print_test()
    import uvicorn
    uvicorn.run('test:app', host="127.0.0.1", port=8000, reload=True)