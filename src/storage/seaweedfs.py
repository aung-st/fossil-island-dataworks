from interface import storage_interface
import boto3

class seaweedfs_storage(storage_interface):

    def __init__(self):
        self.endpoint_url="http://localhost:8333"

    def store_data(self,key,data):
        pass
    
    def get_data(self,key):
        pass

    def list_stored_data(self):
        pass