
import pytest

from src.warehouse.postgres import postgres_warehouse


@pytest.fixture
def postgres():
    return postgres_warehouse()


@pytest.fixture
def mock_postgres(mocker):
    return mocker.MagicMock()


def test_table_created_if_not_exists(postgres, mock_postgres):
    postgres.connection = mock_postgres

    cursor = mock_postgres.cursor.return_value.__enter__.return_value

    postgres.create_schema()

    cursor.execute.assert_called_once()

    query = cursor.execute.call_args.args[0]

    assert "CREATE TABLE IF NOT EXISTS latest_trades" in query

    mock_postgres.commit.assert_called_once()


def test_table_row_data_fetched(postgres, mock_postgres):
    postgres.connection = mock_postgres

    cursor = mock_postgres.cursor.return_value.__enter__.return_value

    mock_id = "1"

    postgres.get_data(mock_id)

    cursor.execute.assert_called_once()

    query = cursor.execute.call_args.args[0]

    assert "SELECT * FROM latest_trades where id = %s" in query


def test_all_table_data_fetched(postgres, mock_postgres):
    postgres.connection = mock_postgres

    cursor = mock_postgres.cursor.return_value.__enter__.return_value

    postgres.get_all_data()

    cursor.execute.assert_called_once()

    query = cursor.execute.call_args.args[0]

    assert "SELECT * FROM latest_trades" in query


def test_table_deletion(postgres, mock_postgres):
    postgres.connection = mock_postgres

    cursor = mock_postgres.cursor.return_value.__enter__.return_value

    postgres.delete_data()

    cursor.execute.assert_called_once()

    query = cursor.execute.call_args.args[0]

    assert "DROP TABLE latest_trades" in query


def test_table_update(postgres, mock_postgres):
    postgres.connection = mock_postgres

    cursor = mock_postgres.cursor.return_value.__enter__.return_value
    mock_id = 123
    mock_data = {
        "examine": "Test examine",
        "members": True,
        "lowalch": 100,
        "limit": 50,
        "value": 200,
        "highalch": 300,
        "icon": "test.png",
        "name": "Test item",
        "high": 500,
        "highTime": 1234567890,
        "low": 400,
        "lowTime": 1234567880,
    }
    postgres.update_data(mock_id, mock_data)

    cursor.execute.assert_called_once()

    query = cursor.execute.call_args.args[0]

    assert (
        """
            UPDATE latest_trades
            SET
                examine = %s,
                members = %s,
                lowalch = %s,
                limit_value = %s,
                value = %s,
                highalch = %s,
                icon = %s,
                name = %s,
                high = %s,
                hightime = %s,
                low = %s,
                lowtime = %s
            WHERE id = %s;
        """
        in query
    )

    mock_postgres.commit.assert_called_once()


def test_table_insertion(postgres, mock_postgres):
    postgres.connection = mock_postgres

    cursor = mock_postgres.cursor.return_value.__enter__.return_value
    mock_data = {
        "examine": "Test examine",
        "id": 2,
        "members": True,
        "lowalch": 100,
        "limit": 50,
        "value": 200,
        "highalch": 300,
        "icon": "test.png",
        "name": "Test item",
        "high": 500,
        "highTime": 1234567890,
        "low": 400,
        "lowTime": 1234567880,
    }
    postgres.store_data(mock_data)

    cursor.execute.assert_called_once()

    query = cursor.execute.call_args.args[0]

    assert (
        """
        INSERT INTO latest_trades (examine, id, members, lowalch, limit_value, value, highalch, icon, name, high, hightime, low, lowtime)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id)
        DO UPDATE SET
            examine = EXCLUDED.examine,
            members = EXCLUDED.members,
            lowalch = EXCLUDED.lowalch,
            limit_value = EXCLUDED.limit_value,
            value = EXCLUDED.value,
            highalch = EXCLUDED.highalch,
            icon = EXCLUDED.icon,
            name = EXCLUDED.name,
            high = EXCLUDED.high,
            hightime = EXCLUDED.hightime,
            low = EXCLUDED.low,
            lowtime = EXCLUDED.lowtime;
        """
        in query
    )

    mock_postgres.commit.assert_called_once()
