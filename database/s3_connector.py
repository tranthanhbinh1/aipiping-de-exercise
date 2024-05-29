import boto3
from configs import S3Config

class S3Connector:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=S3Config.S3_ACCESS_KEY,
            aws_secret_access_key=S3Config.S3_SECRET_KEY,
            endpoint_url="http://localhost:9000",
            use_ssl=False,
        )
        
    def get_object(self, bucket: str, key: str) -> None:
        return self.s3.get_object(Bucket=bucket, Key=key)
    
    def put_object(self, bucket: str, key: str, body: str) -> None:
        return self.s3.put_object(Bucket=bucket, Key=key, Body=body)
