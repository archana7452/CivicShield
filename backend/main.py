from fastapi import FastAPI

from backend.database import engine
from backend.routes import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def home():
    try:
        with engine.connect():
            return {"message": "CivicShield Backend + MySQL connected"}
    except Exception as e:
        return {"error": str(e)}