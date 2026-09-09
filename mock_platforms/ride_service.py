from fastapi import FastAPI

app = FastAPI()

@app.post("/restriction")
def receive_restriction(data: dict):
    return {
        "platform": "RIDE_HAILING",
        "status": "RESTRICTED",
        "message": "⚠️ Ride service temporarily unavailable in this area.",
        "reason": "Public safety restriction active."
    }

@app.get("/")
def home():
    return {
        "platform": "RIDE_HAILING",
        "status": "ACTIVE"
    }