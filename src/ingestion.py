import requests 
import os


ITEM_ENDPOINT = os.getenv("ITEM_ENDPOINT")
PRICE_ENDPOINT = os.getenv("PRICE_ENDPOINT")

headers = {
    "User-Agent": "fossil-island-dataworks"
}

def ingest_item_mapping():
    response = requests.get(ITEM_ENDPOINT, headers=headers)
    return response.json()

def ingest_latest_prices():
    response = requests.get(PRICE_ENDPOINT, headers=headers)
    return response.json()
