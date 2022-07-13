from typing import Tuple
from fastapi import FastAPI
import weather


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(weather.router)