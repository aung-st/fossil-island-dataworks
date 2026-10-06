import logging
from os import getenv

import psycopg2

from src.warehouse.interface import warehouse_interface

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class postgres_warehouse(warehouse_interface):
    def __init__(self):

        self.POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
        self.POSTGRES_DB = getenv("POSTGRES_DB")
        self.POSTGRES_USER = getenv("POSTGRES_USER")
        self.POSTGRES_HOST = getenv("POSTGRES_HOST")
        self.POSTGRES_PORT = getenv("POSTGRES_PORT")

        self.connection = psycopg2.connect(
            dbname=self.POSTGRES_DB,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
        )

    def create_schema(self) -> None:
        create_latest_table_query = """CREATE TABLE IF NOT EXISTS latest_trades (
            id INTEGER PRIMARY KEY,
            examine TEXT,
            members BOOLEAN,
            lowalch INTEGER,
            limit_value INTEGER,
            value INTEGER,
            highalch INTEGER,
            icon TEXT,
            name TEXT,
            high BIGINT,
            hightime BIGINT,
            low BIGINT,
            lowtime BIGINT
        );
        """

        logger.info("Creating the latest trades table if it does not already exist")
        with self.connection.cursor() as cursor:
            cursor.execute(create_latest_table_query)
            self.connection.commit()

    def store_data(self, data: dict) -> None:

        store_data_query = """
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

        logger.debug(
            f"Storing joined data row with id {data['id']} into latest items table"
        )

        with self.connection.cursor() as cursor:
            cursor.execute(
                store_data_query,
                (
                    data["examine"],
                    data["id"],
                    data["members"],
                    data.get("lowalch"),
                    data.get("limit"),
                    data["value"],
                    data.get("highalch"),
                    data["icon"],
                    data["name"],
                    data["high"],
                    data["highTime"],
                    data["low"],
                    data["lowTime"],
                ),
            )

            self.connection.commit()

    def get_data(self, id: int) -> tuple:
        get_data_row_query = "SELECT * FROM latest_trades where id = %s"

        logger.info(f"Getting data row with id {id}")

        with self.connection.cursor() as cursor:
            cursor.execute(get_data_row_query, (id,))
            row = cursor.fetchone()

        return row

    def get_all_data(self) -> list[tuple]:
        get_all_data_rows_query = "SELECT * FROM latest_trades"

        logger.info("Getting all rows from latest trades table")
        with self.connection.cursor() as cursor:
            cursor.execute(get_all_data_rows_query)
            row = cursor.fetchall()

        return row

    def update_data(self, id: int, data: dict) -> None:
        update_data_query = """
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

        logger.info("Updating item id {id}")
        with self.connection.cursor() as cursor:
            cursor.execute(
                update_data_query,
                (
                    data["examine"],
                    data["members"],
                    data["lowalch"],
                    data["limit"],
                    data["value"],
                    data["highalch"],
                    data["icon"],
                    data["name"],
                    data["high"],
                    data["highTime"],
                    data["low"],
                    data["lowTime"],
                    id,
                ),
            )

            self.connection.commit()

    def delete_data(self) -> None:
        delete_data_query = """
        DROP TABLE latest_trades
        """

        logger.info("Deleting latest tables")
        with self.connection.cursor() as cursor:
            cursor.execute(delete_data_query, (id,))
