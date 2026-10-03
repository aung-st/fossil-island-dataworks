from os import getenv

import boto3

from src.storage.interface import storage_interface


class seaweedfs_storage(storage_interface):
    def __init__(self):
        endpoint_url = getenv("ENDPOINT_URL")
        aws_access_key_id = getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = getenv("AWS_SECRET_ACCESS_KEY")
        self.s3 = boto3.client(
            service_name="s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.bucket = "osrs-data"

    # Technically a list or a dict for data but the json util will stringify it
    def store_data(self, key: str, data: str) -> None:
        self.s3.put_object(Body=data, Bucket=self.bucket, Key=key)

    def get_data(self, key: str) -> dict:

        # We will realistically only take the latest snapshot for transforming via a helper
        # objects_list = self.list_stored_data(prefix)
        # key = objects_list["Contents"][0]["Key"]

        return self.s3.get_object(Bucket=self.bucket, Key=key)

    def list_stored_data(self, prefix: str) -> dict:

        objects_list = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)

        # sort to get latest snapshot
        objects_list["Contents"].sort(key=lambda obj: obj["Key"], reverse=True)
        return objects_list
