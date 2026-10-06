import pytest

from src.storage.seaweedfs import seaweedfs_storage


@pytest.fixture
def seaweed():
    return seaweedfs_storage()


@pytest.fixture
def mock_seaweed(mocker):
    return mocker.Mock()


@pytest.mark.unit
def test_list_stored_data_mappings_path_is_correct(seaweed, mock_seaweed):
    seaweed.s3 = mock_seaweed

    mock_seaweed.list_objects_v2.return_value = {"Contents": []}

    seaweed.list_stored_data("mappings/")

    mock_seaweed.list_objects_v2.assert_called_once_with(
        Bucket="osrs-data", Prefix="mappings/"
    )


@pytest.mark.unit
def test_list_stored_data_prices_path_is_correct(seaweed, mock_seaweed):
    seaweed.s3 = mock_seaweed

    mock_seaweed.list_objects_v2.return_value = {"Contents": []}

    seaweed.list_stored_data("prices/")

    mock_seaweed.list_objects_v2.assert_called_once_with(
        Bucket="osrs-data", Prefix="prices/"
    )


@pytest.mark.unit
def test_mappings_insertion_path_is_correct(seaweed, mock_seaweed):
    seaweed.s3 = mock_seaweed

    seaweed.store_data("mappings/123.json", "items")

    mock_seaweed.put_object.assert_called_once_with(
        Body="items", Bucket="osrs-data", Key="mappings/123.json"
    )


@pytest.mark.unit
def test_prices_insertion_path_is_correct(seaweed, mock_seaweed):
    seaweed.s3 = mock_seaweed

    seaweed.store_data("prices/123.json", "price")

    mock_seaweed.put_object.assert_called_once_with(
        Body="price", Bucket="osrs-data", Key="prices/123.json"
    )


@pytest.mark.unit
def test_list_stored_data_sorts_by_time_descending(seaweed, mock_seaweed):
    seaweed.s3 = mock_seaweed

    mock_seaweed.list_objects_v2.return_value = {
        "Contents": [
            {"Key": "mappings/1791018717_item_mapping_data.json"},
            {"Key": "mappings/1791018713_item_mapping_data.json"},
            {"Key": "mappings/1791018718_item_mapping_data.json"},
        ]
    }

    mocked_response = seaweed.list_stored_data("mappings/")

    assert (
        mocked_response["Contents"][0]["Key"]
        == "mappings/1791018718_item_mapping_data.json"
    )
    assert (
        mocked_response["Contents"][1]["Key"]
        == "mappings/1791018717_item_mapping_data.json"
    )
    assert (
        mocked_response["Contents"][2]["Key"]
        == "mappings/1791018713_item_mapping_data.json"
    )


@pytest.mark.unit
def test_get_data_grabs_specified_filepath(seaweed, mock_seaweed):
    seaweed.s3 = mock_seaweed

    seaweed.get_data("mappings/123.json")

    mock_seaweed.get_object.assert_called_once_with(
        Bucket="osrs-data", Key="mappings/123.json"
    )
