from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import router
from api.dependencies import (
    get_repository,
    get_matcher,
    get_recommender,
)
from download_dataset import download_dataset


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("=" * 60)
    print("Starting LB Rec API...")
    print("=" * 60)

    import os
    import psutil

    process = psutil.Process(os.getpid())

    def log_ram(stage):
        print(f"{stage}: {process.memory_info().rss / 1024 / 1024:.2f} MB")

    download_dataset()
    log_ram("After dataset check")

    get_repository()
    log_ram("After repository")

    get_matcher()
    log_ram("After matcher")

    get_recommender()
    log_ram("After recommender")

    print("=" * 60)
    print("API Ready")
    print("=" * 60)

    yield

    print("Shutting down...")


app = FastAPI(
    title="LB Rec API",
    description="Letterboxd Movie Recommendation API",
    version="1.1",
    lifespan=lifespan
)

app.include_router(router)


@app.get("/")
def home():

    return {
        "message": "LB Rec API is running."
    }