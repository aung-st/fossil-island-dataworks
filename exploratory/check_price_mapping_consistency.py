def check_price_mapping_consistency(self, mappings, prices):
    price_ids = {item["id"] for item in prices}
    mapping_ids = {item["id"] for item in mappings}

    missing_mappings = price_ids - mapping_ids
    missing_prices = mapping_ids - price_ids

    return (missing_mappings, missing_prices)
