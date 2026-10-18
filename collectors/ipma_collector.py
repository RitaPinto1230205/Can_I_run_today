"""
IPMA collector: fetches the weather forecast for Porto and stores the raw
response in MongoDB, exactly as it arrives. Cleaning happens later (Day 2).

Run:  python collectors/ipma_collector.py
"""

import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Porto's id in the IPMA API (from distrits-islands.json)
PORTO_ID = 1131200

FORECAST_URL = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{id}.json"

MONGO_URI = (
    f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}"
    f"@localhost:27017"
)


def fetch_forecast(location_id: int) -> dict:
    """Call the IPMA API and return the JSON response."""
    url = FORECAST_URL.format(id=location_id)
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def save_raw(document: dict) -> None:
    """Store the raw response in MongoDB, collection 'ipma_raw'."""
    with MongoClient(MONGO_URI) as client:
        collection = client["correhoje"]["ipma_raw"]
        collection.insert_one(document)


def main() -> None:
    data = fetch_forecast(PORTO_ID)

    # We wrap the response with metadata: where it came from and when.
    # This is what lets you debug the pipeline later.
    document = {
        "source": "ipma",
        "location_id": PORTO_ID,
        "fetched_at": datetime.now(timezone.utc),
        "payload": data,
    }
    save_raw(document)
    print(f"Saved IPMA forecast at {document['fetched_at']}")


if __name__ == "__main__":
    main()