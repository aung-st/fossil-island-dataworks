import logging
from os import getenv

import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ITEM_ENDPOINT = getenv("ITEM_ENDPOINT")
PRICE_ENDPOINT = getenv("PRICE_ENDPOINT")

headers = {"User-Agent": "fossil-island-dataworks"}


def ingest_item_mapping() -> list:
    response = requests.get(ITEM_ENDPOINT, headers=headers)
    logger.info(f"Mapping request made with status {response.status_code}")
    return response.json()


def ingest_latest_prices() -> dict:
    response = requests.get(PRICE_ENDPOINT, headers=headers)
    logger.info(f"Prices request made with status {response.status_code}")
    return response.json()
