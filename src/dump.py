from ingestion import ingest_item_mapping,ingest_latest_prices
import json 

dump_filepath = "data/"

def dump_mappings():
    data = ingest_item_mapping()
    with open(f"{dump_filepath}item_mapping_data.json","w") as item_mapping_data:
        json.dump(data,item_mapping_data)


def dump_prices():
    data = ingest_item_mapping()
    with open(f"{dump_filepath}prices_data.json","w") as prices_data:
        json.dump(data,prices_data)
