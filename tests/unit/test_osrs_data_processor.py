import pytest

from src.etl.osrs_data_processor import osrs_data_processor


@pytest.fixture
def processor():
    return osrs_data_processor()


def test_get_key(processor, mocker):

    mock_list = mocker.patch.object(
        processor.seaweed,
        "list_stored_data",
        return_value={"Contents": [{"Key": "prices/123.json"}]},
    )

    key = processor.get_key("prices/")

    assert key == "prices/123.json"

    mock_list.assert_called_once_with("prices/")


def test_get_prices_file(processor, mocker):

    mocker.patch.object(
        processor.seaweed,
        "get_data",
        return_value={
            "Body": mocker.Mock(
                read=mocker.Mock(
                    return_value=b'{"data": [{"id": 2, "name": "Steel cannonball"}]}'
                )
            )
        },
    )

    file = processor.get_file("prices/123.json")

    assert file == {"data": [{"id": 2, "name": "Steel cannonball"}]}


def test_normalise_prices(processor, mocker):

    mocker.patch.object(
        processor.seaweed,
        "get_data",
        return_value={
            "Body": mocker.Mock(
                read=mocker.Mock(
                    return_value=b'{"data": {"2": {"high": 290, "highTime": 1791280256, "low": 277, "lowTime": 1791280205}}}'
                )
            )
        },
    )

    normalised_data = processor.normalise_prices("prices/123.json")

    expected_shape = [
        (
            "2",
            {
                "high": 290,
                "highTime": 1791280256,
                "low": 277,
                "lowTime": 1791280205,
            },
        )
    ]

    assert type(normalised_data) is list
    assert normalised_data == expected_shape


def test_transform_normalised_prices(processor):

    mock_normalised_prices = [
        (
            "2",
            {
                "high": 290,
                "highTime": 1791280256,
                "low": 277,
                "lowTime": 1791280205,
            },
        )
    ]

    expected_shape = [
        {
            "id": 2,
            "high": 290,
            "highTime": 1791280256,
            "low": 277,
            "lowTime": 1791280205,
        }
    ]

    transformed_prices = processor.transform_normalised_prices(mock_normalised_prices)

    assert type(transformed_prices) is list
    assert transformed_prices == expected_shape


def test_get_valid_tradeable_items(processor):

    mock_mapping = [
        {
            "id": 2,
            "name": "Steel cannonball",
            "members": False,
            "lowalch": 2,
            "limit": 11000,
            "value": 5,
            "highalch": 3,
            "icon": "Steel cannonball.png",
            "examine": "Ammo suited for a boat's cannon or for a dwarf multicannon.",
        },
        {
            "id": 3,
            "name": "Cannonball",
            "members": False,
            "lowalch": 1,
            "limit": 11000,
            "value": 5,
            "highalch": 2,
            "icon": "Cannonball.png",
            "examine": "Ammo for a cannon.",
        },
    ]

    mock_prices = [
        {
            "id": 2,
            "high": 290,
            "highTime": 1791280256,
            "low": 277,
            "lowTime": 1791280205,
        }
    ]

    valid_items = processor.get_valid_tradeable_items(mock_mapping, mock_prices)

    assert type(valid_items) is set
    assert valid_items == {2}


def test_joined_data(processor):

    mock_mapping = [
        {
            "id": 2,
            "name": "Steel cannonball",
            "members": False,
            "lowalch": 2,
            "limit": 11000,
            "value": 5,
            "highalch": 3,
            "icon": "Steel cannonball.png",
            "examine": "Ammo suited for a boat's cannon or for a dwarf multicannon.",
        }
    ]

    mock_prices = [
        {
            "id": 2,
            "high": 290,
            "highTime": 1791280256,
            "low": 277,
            "lowTime": 1791280205,
        }
    ]

    expected_joined_data = [
        {
            "id": 2,
            "name": "Steel cannonball",
            "members": False,
            "lowalch": 2,
            "limit": 11000,
            "value": 5,
            "highalch": 3,
            "icon": "Steel cannonball.png",
            "examine": "Ammo suited for a boat's cannon or for a dwarf multicannon.",
            "high": 290,
            "highTime": 1791280256,
            "low": 277,
            "lowTime": 1791280205,
        }
    ]

    joined_data = processor.join_data(mock_mapping, mock_prices)

    assert joined_data == expected_joined_data
