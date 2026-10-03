from json import dumps 

from src.storage.seaweedfs import seaweedfs_storage

from src.ingestion import ingest_item_mapping, ingest_latest_prices

from time import time

seaweed = seaweedfs_storage()
unix_timestamp = int(time())
mapping_filename = "item_mapping_data.json"
prices_filename = "prices_data.json"

def dump_mappings():
    data = dumps(ingest_item_mapping())

    seaweed.store_data(key=f"mappings/{unix_timestamp}_{mapping_filename}",data = data)

def dump_prices():
    data = dumps(ingest_latest_prices())
    seaweed.store_data(key=f"prices/{unix_timestamp}_{prices_filename}",data = data)

dump_mappings()
dump_prices()