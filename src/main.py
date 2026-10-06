from time import time

from src.etl.osrs_data_processor import osrs_data_processor
from src.lib.dump import dump_mappings, dump_prices
from src.warehouse.postgres import postgres_warehouse

if __name__ == "__main__":
    unix_timestamp = int(time())
    dump_mappings(unix_timestamp)
    dump_prices(unix_timestamp)

    osrs_data = osrs_data_processor()

    prices_key = osrs_data.get_key("prices/")
    mappings_key = osrs_data.get_key("mappings/")

    normalised_prices = osrs_data.normalise_prices(prices_key)

    prices = osrs_data.transform_normalised_prices(normalised_prices)
    mappings = osrs_data.get_file(mappings_key)

    joined_data = osrs_data.join_data(mappings, prices)

    postgres_warehouse = postgres_warehouse()

    postgres_warehouse.delete_data()
    postgres_warehouse.create_schema()

    for row in joined_data:
        postgres_warehouse.store_data(data=row)

    data = postgres_warehouse.get_all_data()

    print(data[0])
