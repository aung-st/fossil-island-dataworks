import logging
from os import getenv

import boto3

from src.storage.interface import storage_interface

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class seaweedfs_storage(storage_interface):
    def __init__(self):
        endpoint_url = getenv("ENDPOINT_URL")
        aws_access_key_id = getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = getenv("AWS_SECRET_ACCESS_KEY")
        s3_bucket = getenv("S3_BUCKET")
        self.s3 = boto3.client(
            service_name="s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.bucket = s3_bucket

    # Technically a list or a dict for data but the json util will stringify it
    def store_data(self, key: str, data: str) -> None:
        self.s3.put_object(Body=data, Bucket=self.bucket, Key=key)
        logger.info("File {key} is now in storage")

    def get_data(self, key: str) -> dict:
        logger.info("Fetching file {key} from storage")
        return self.s3.get_object(Bucket=self.bucket, Key=key)

    def list_stored_data(self, prefix: str) -> dict:

        logger.info("Fetching object list from {prefix}")
        objects_list = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
        # sort to get latest snapshot

        logger.info("Sorting object list")
        objects_list["Contents"].sort(key=lambda obj: obj["Key"], reverse=True)
        return objects_list
