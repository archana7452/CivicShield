from fastapi import FastAPI

app = FastAPI()

@app.post("/restriction")
def receive_restriction(data: dict):
    return {
        "platform": "GROCERY_DELIVERY",
        "status": "RESTRICTED",
        "message": "⚠️ Grocery delivery temporarily unavailable in this area.",
        "reason": "Public safety restriction active."
    }

@app.get("/")
def home():
    return {
        "platform": "GROCERY_DELIVERY",
        "status": "ACTIVE"
    }