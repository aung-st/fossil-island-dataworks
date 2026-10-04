from json import loads

from src.storage.seaweedfs import seaweedfs_storage


class osrs_data_processor:
    def __init__(self):
        self.seaweed = seaweedfs_storage()

    def get_key(self, prefix):

        # We take the latest snapshot for transforming

        file_list = self.seaweed.list_stored_data(prefix)
        file_key = file_list["Contents"][0]["Key"]

        return file_key

    def get_file(self, key):

        data = self.seaweed.get_data(key)
        data = data["Body"].read()
        data = loads(data.decode("utf-8"))
        return data

    def normalise_prices(self, key):

        data = self.get_file(key)["data"]

        return list(data.items())

    def transform_normalised_prices(self, normalised_prices):

        transformed_prices = []

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
