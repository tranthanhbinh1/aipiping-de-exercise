import requests
import logging
import json
import asyncio
from typing import Optional
from database.models.lead import Lead
from database.models.linkedin_data import Linkedin
from database.s3_connector import S3Connector
from database.mongodb_connector import init
from utils.logging_config import setup_logging
from configs import LINKEDIN_BUCKET, MONGODB_DB_NAME

setup_logging()


class ELT:
    linkedin_api = "http://127.0.0.1:8000/get_linkedin_data/abc@gmail.com"

    def __init__(self) -> None:
        self.s3_connector = S3Connector()
        self.data: Optional[dict] = self.extract()
        self.mongodb_conn = None

    @classmethod
    def extract(cls) -> dict:
        try:
            resp = requests.get(cls.linkedin_api)
            logging.info("Extracted data from LinkedIn")
            return resp.json()
        except Exception as e:
            logging.error(f"Failed to extract data from LinkedIn: {e}")
            return {}

    def load(self) -> None:
        json_data = json.dumps(self.data).encode()
        # Upload the raw data to s3
        self.s3_connector.put_object(
            bucket=LINKEDIN_BUCKET, key="raw.json", body=json_data
        )

    async def async_load(self) -> None:
        await init(database=MONGODB_DB_NAME, document_models=[Lead, Linkedin])
        # Insert the raw data to mongodb

        if self.data is not None:
            raw_linkedin_data = Linkedin(
                credits_left=self.data["credits_left"],
                person=self.data["person"],
                rate_limit_left=self.data["rate_limit_left"],
                success=self.data["success"],
            )
            await raw_linkedin_data.insert()
            logging.info("Successfully inserted!")

        else:
            logging.info("No data")

    def transform(self, data: dict) -> Optional[dict]:
        pass


if __name__ == "__main__":
    elt = ELT()
    asyncio.run(elt.async_load())
    # logging.info(data)
