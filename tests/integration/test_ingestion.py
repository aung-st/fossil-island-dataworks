import pytest

from src.ingestion import ingest_item_mapping, ingest_latest_prices


@pytest.mark.integration
def test_good_mapping_payload():
    assert type(ingest_item_mapping()) is list


@pytest.mark.integration
def test_good_prices_payload():
    assert type(ingest_latest_prices()) is dict
