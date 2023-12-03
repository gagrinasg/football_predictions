from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

def poll_api():
    # Place your API polling logic here
    print("Polling API...")

# Create a scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(poll_api, "interval", seconds=15)
scheduler.start()

# You can stop the scheduler when the FastAPI app stops
@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
