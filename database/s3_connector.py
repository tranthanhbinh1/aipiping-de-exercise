import boto3
import logging
from utils.logging_config import setup_logging
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
        setup_logging()

    def get_object(self, bucket: str, key: str) -> None:
        try:
            self.s3.get_object(Bucket=bucket, Key=key)
            logging.info(f"Successfully get object {key}")
        except Exception as e:
            logging.error(f"Failed to get object {object}, error: {repr(e)}")

    def put_object(self, bucket: str, key: str, body: object) -> None:
        return self.s3.put_object(Bucket=bucket, Key=key, Body=body)
