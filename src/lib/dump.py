import json

from seaweedfs import seaweedfs_storage

from src.ingestion import ingest_item_mapping

dump_filepath = "data/"

seaweed = seaweedfs_storage()


def dump_mappings():
    data = ingest_item_mapping()
    with open(f"{dump_filepath}item_mapping_data.json", "w") as item_mapping_data:
        json.dump(data, item_mapping_data)


def dump_prices():
    data = ingest_item_mapping()
    with open(f"{dump_filepath}prices_data.json", "w") as prices_data:
        json.dump(data, prices_data)
