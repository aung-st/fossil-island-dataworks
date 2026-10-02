from interface import storage_interface
import boto3

class seaweedfs_storage(storage_interface):

    def __init__(self):
        self.endpoint_url="http://localhost:8333"
        self.s3 = boto3.client(service_name="s3", endpoint_url = self.endpoint_url, aws_access_key_id="dummy", aws_secret_access_key="dummy")
        self.bucket = "osrs-data"

    def store_data(self,key,data):
        self.s3.put_object(Body=data, Bucket=self.bucket, Key=key)
    
    # We will realistically only take the latest snapshot for transforming
    def get_data(self,key):

        # objects_list = self.list_stored_data(prefix)
        
        # key = objects_list["Contents"][0]["Key"]

        return self.s3.get_object(Bucket=self.bucket,Key=key)

    def list_stored_data(self,prefix):

        objects_list = self.s3.list_objects_v2(Bucket=self.bucket,Prefix=prefix)

        # sort to get latest snapshot
        objects_list["Contents"].sort(key = lambda obj: obj["Key"], reverse = True)
        return objects_list