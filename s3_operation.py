import boto3
from PIL import Image
import io
import json


with open("private.json","r") as f:
    file = json.load(f)
aws_access_key_id = file["aws_access_key_id"]
aws_secret_access_key = file["aws_secret_access_key"]




class s3_class:
    def __init__(self):
        # self.region= "us-east-2"
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key


    def create_conn_to_s3(self,region_name):
        try:
            re = boto3.resource("s3",region_name=region_name,aws_access_key_id=self.aws_access_key_id,aws_secret_access_key=self.aws_secret_access_key)
            return re
        except Exception as e:
            raise e

    def delete_all_objects_in_bucket(self,region_name, bucket_name):
        try:
            re = self.create_conn_to_s3(region_name)
            buck = re.Bucket(bucket_name)
            res = buck.objects.all().delete()
        except Exception as e:
            raise e

    def getting_list_of_objs_from_buckets(self,region_name,bucket_name):
        try:
            lis = []
            re = self.create_conn_to_s3(region_name)
            buck = re.Bucket(bucket_name)
            for i in buck.meta.client.list_objects(Bucket=bucket_name).get('Contents', None):
                lis.append(i.get('Key', None))
            return lis
        except Exception as e:
            raise e

    def read_img_from_s3_in_RAM(self,region_name, bucket_name, key,size_tuple):
        try:
            s3 = self.create_conn_to_s3(region_name)
            bucket = s3.Bucket(bucket_name)
            obj = bucket.meta.client.get_object(Bucket=bucket_name, Key=key)
            body = obj.get("Body", None).read()
            img = Image.open(io.BytesIO(body))
            im = img.resize(size=size_tuple)
            return im
        except Exception as e:
            raise e
            








