from fastapi import FastAPI
import weather


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from Nebraska.Code"}

@app.get("/something")
async def something(name: int):
    return {f"Hello, {name}!!!"}

app.include_router(weather.router)