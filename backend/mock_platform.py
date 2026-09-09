from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="CivicShield Mock Platform API",
    version="1.0"
)


class PlatformRestriction(BaseModel):

    platform: str
    zone_id: int
    status: str
    reason: str


@app.get("/")
def home():

    return {
        "success": True,
        "message": "Mock Platform API is running"
    }


@app.post("/api/platform/restriction")
def receive_restriction(
    restriction: PlatformRestriction
):

    return {

        "success": True,

        "message": "Platform received safety restriction",

        "data": {

            "platform": restriction.platform,

            "zone_id": restriction.zone_id,

            "status": restriction.status,

            "reason": restriction.reason

        }

    }