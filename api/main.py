from fastapi import FastAPI

from api.routes import router


app = FastAPI(

    title="LB Rec API",

    description="Letterboxd Movie Recommendation API",

    version="1.1"

)


app.include_router(router)


@app.get("/")
def home():

    return {

        "message": "LB Rec API is running."

    }