## Export requirements.txt 
poetry export --without-hashes --format=requirements.txt > requirements.txt

## What docker runs
uvicorn main:app --host 0.0.0.0 --port 8000

## what you should run on the main dir
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

## Docker build image from app
docker build -t football-prediction:latest .

## run docker container
docker run -p 8000:8000 --rm --name your-fastapi-container your-fastapi-image:tag

# Run compose in order to build the local image as well
docker compose up --build -d