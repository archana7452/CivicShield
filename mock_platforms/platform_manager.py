import requests

PLATFORMS = {
    "FOOD_DELIVERY": "http://127.0.0.1:8001/restriction",
    "RIDE_HAILING": "http://127.0.0.1:8002/restriction",
    "GROCERY_DELIVERY": "http://127.0.0.1:8003/restriction"
}

def send_restriction_to_platforms(restriction):
    results = []

    for platform, url in PLATFORMS.items():
        try:
            response = requests.post(
                url,
                json=restriction,
                timeout=5
            )

            results.append({
                "platform": platform,
                "status": "SENT",
                "response": response.json()
            })

        except Exception as e:
            results.append({
                "platform": platform,
                "status": "FAILED",
                "error": str(e)
            })

    return results