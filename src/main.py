from src.lib.dump import dump_mappings, dump_prices
from time import time 

if __name__ == "__main__":
    unix_timestamp = int(time())
    dump_mappings(unix_timestamp)
    dump_prices(unix_timestamp)
