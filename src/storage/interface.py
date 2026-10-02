from abc import abstractmethod


class storage_interface:
    @abstractmethod
    def store_data(self, key, data):
        pass

    @abstractmethod
    def get_data(self, key):
        pass

    @abstractmethod
    def list_stored_data(self):
        pass
