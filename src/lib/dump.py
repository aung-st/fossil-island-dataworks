import logging
from json import dumps

from src.ingestion import ingest_item_mapping, ingest_latest_prices
from src.storage.seaweedfs import seaweedfs_storage

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

seaweed = seaweedfs_storage()
mapping_filename = "item_mapping_data.json"
prices_filename = "prices_data.json"


def dump_mappings(unix_timestamp) -> None:
    data = dumps(ingest_item_mapping())

    logger.info("Preparing to dump mappings")
    seaweed.store_data(key=f"mappings/{unix_timestamp}_{mapping_filename}", data=data)


def dump_prices(unix_timestamp) -> None:
    data = dumps(ingest_latest_prices())

    logger.info("Preparing to dump prices")
    seaweed.store_data(key=f"prices/{unix_timestamp}_{prices_filename}", data=data)
