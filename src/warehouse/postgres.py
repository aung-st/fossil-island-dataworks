from src.warehouse.interface import warehouse_interface


class seaweedfs_storage(warehouse_interface):
    def __init__(self):
        pass

    def store_data(self, key: str, data: str) -> None:
        pass

    def get_data(self, key: str) -> dict:
        pass

    def list_stored_data(self, prefix: str) -> dict:
        pass
