import requests
import logging
import json
import asyncio
from beanie import Document
from typing import Optional, Any
from database.models.lead import Lead, LeadView
from database.models.linkedin_data import Linkedin
from database.s3_connector import S3Connector
from database.mongodb_connector import init
from utils.logging_config import setup_logging
from configs import LINKEDIN_BUCKET, MONGODB_DB_NAME

setup_logging()


class ELT:
    """
    ELT (Extract, Load, Transform) class for data processing.

    This class is responsible for extracting data from the LinkedIn API,
    loading the raw data into an S3 bucket, and transforming the raw data
    into a Lead document in MongoDB.

    Attributes:
        linkedin_api (str): The URL of the LinkedIn API.
        s3_connector (S3Connector): An instance of the S3Connector class.
        data (Optional[dict]): The extracted data from LinkedIn API.
        mongodb_conn: The MongoDB connection object.

    Methods:
        extract: Extracts data from LinkedIn API.
        load: Loads the raw data into S3.
        async_load: Loads the raw data into MongoDB.
        transform: Transforms the raw data into a Lead document.

    """

    default_linkedin_api = "http://127.0.0.1:8000/get_linkedin_data/{email}"

    def __init__(self, email: str) -> None:
        self.email = email
        self.s3_connector = S3Connector()
        self.data: Optional[dict] = self.extract()
        self.mongodb_conn = None
        self.linkedin_api: str = self.default_linkedin_api.format(email=self.email)
        self.doc: Optional[Document] = None

    # @classmethod
    def extract(self) -> dict:
        """
        Extracts data from LinkedIn API.

        Returns:
            dict: The extracted data from LinkedIn API.
        """
        try:
            resp = requests.get(self.linkedin_api)
            logging.info("Extracted data from LinkedIn")
            return resp.json()
        except Exception as e:
            logging.error(f"Failed to extract data from LinkedIn: {e}")
            return {}

    def load_s3(self) -> None:
        """
        Loads the raw data into S3.

        This method converts the raw data to JSON format and uploads it to
        the specified S3 bucket.

        Returns:
            None
        """
        json_data = json.dumps(self.data).encode()
        # Upload the raw data to s3
        self.s3_connector.put_object(
            bucket=LINKEDIN_BUCKET, key="raw.json", body=json_data
        )

    async def async_load_mongo_raw(self) -> None:
        """
        Loads the raw data into MongoDB.

        This method initializes the database and inserts the raw data into the
        MongoDB collection. If there is no data available, it logs a message.

        Returns:
            None
        """
        await init(database=MONGODB_DB_NAME, document_models=[Linkedin])
        # Insert the raw data to mongodb

        if self.data:
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

    async def transform(self) -> Any:
        """
        Transforms the raw data from the Linkedin collection to a Lead document.

        Returns:
            Any: The result of the transformation process.
        """
        await init(database=MONGODB_DB_NAME, document_models=[Linkedin, Lead])

        # Transform the raw data to a Lead document
        result = await Linkedin.find().sort("-_id").project(LeadView).limit(1).to_list()
        if result:
            logging.info(f"Found and Transformed {len(result)} documents")
            self.doc = Lead(
                status=result[0].status,
                first_name=result[0].first_name,
                last_name=result[0].last_name,
                email=result[0].email,
                photo_url=result[0].photo_url,
            )
        logging.info(result[0])

    async def load_mongo_transformed(self) -> None:
        """
        Loads the transformed data into MongoDB.

        This method inserts the transformed data into the MongoDB collection.

        Returns:
            None
        """
        await init(database=MONGODB_DB_NAME, document_models=[Lead])
        if self.doc:
            await self.doc.insert()
            logging.info("Successfully inserted!")
        else:
            logging.info("No data")

    def main(self) -> None:
        self.extract()
        self.load_s3()
        asyncio.run(self.async_load_mongo_raw())
        asyncio.run(self.transform())
        asyncio.run(self.load_mongo_transformed())


if __name__ == "__main__":
    elt = ELT(email="abc@gmail.com")
    elt.main()
