import logging
from json import loads

from src.storage.seaweedfs import seaweedfs_storage

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class osrs_data_processor:
    def __init__(self):
        self.seaweed = seaweedfs_storage()

    def get_key(self, prefix: str) -> str:

        # We take the latest snapshot for transforming

        logger.info("Checking for latest snapshot from {prefix}")
        file_list = self.seaweed.list_stored_data(prefix)
        file_key = file_list["Contents"][0]["Key"]

        return file_key

    def get_file(self, key: str) -> list | dict:

        logger.info("Grabbing file {key}")
        data = self.seaweed.get_data(key)
        data = data["Body"].read()
        data = loads(data.decode("utf-8"))
        return data

    def normalise_prices(self, key: str) -> list:

        logger.info("Reshaping prices into a list")
        data = self.get_file(key)["data"]

        return list(data.items())

    def transform_normalised_prices(self, normalised_prices: list) -> list:

        transformed_prices = []

        logger.info("Transforming normalised prices to match shape of mappings")
        for item in normalised_prices:
            transformed_prices.append(
                {
                    "id": int(item[0]),
                    "high": item[1]["high"],
                    "highTime": item[1]["highTime"],
                    "low": item[1]["low"],
                    "lowTime": item[1]["lowTime"],
                }
            )

        return transformed_prices

    def get_valid_tradeable_items(self, mappings: list, normalised_prices: list) -> set:

        logger.info("Fetching all ids for tradeable items that exist in the mappings")
        price_ids = {item["id"] for item in normalised_prices}
        mapping_ids = {item["id"] for item in mappings}
        return price_ids & mapping_ids

    def join_data(self, mappings: list, normalised_prices: list) -> dict:
        joined_data = []

        valid_mappings = self.get_valid_tradeable_items(mappings, normalised_prices)

        logger.info("Inner joining mappings and normalised prices")
        mapping_by_id = {row["id"]: row for row in mappings}
        price_by_id = {row["id"]: row for row in normalised_prices}

        for id in valid_mappings:
            joined_data.append({**mapping_by_id[id], **price_by_id[id]})

        return joined_data
