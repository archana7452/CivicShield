from fastapi import FastAPI

app = FastAPI()

@app.post("/restriction")
def receive_restriction(data: dict):
    return {
        "platform": "FOOD_DELIVERY",
        "status": "RESTRICTED",
        "message": "⚠️ Service temporarily unavailable in this area.",
        "reason": "Public safety restriction active."
    }

@app.get("/")
def home():
    return {
        "platform": "FOOD_DELIVERY",
        "status": "ACTIVE"
    }