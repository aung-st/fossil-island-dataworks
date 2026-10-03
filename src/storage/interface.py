from abc import abstractmethod


class storage_interface:
    @abstractmethod
    def store_data(self, key: str, data: str) -> None:
        pass

    @abstractmethod
    def get_data(self, key: str) -> dict:
        pass

    @abstractmethod
    def list_stored_data(self, prefix: str) -> dict:
        pass
