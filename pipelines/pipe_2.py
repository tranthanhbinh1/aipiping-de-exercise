import requests
import logging
from database import s3_connector
from utils.logging_config import setup_logging  

setup_logging() 

class ELT:
    def __init__(self) -> None:
        self.s3_connector = s3_connector.S3Connector()
        
        
    def extract(self) -> dict:
        try:
            data = requests.get("http://127.0.0.1:8000/get_linkedin_data/abc@gmail.com")
            logging.info("Extracted data from LinkedIn")
            return data.json()
        except Exception as e:
            logging.error(f"Failed to extract data from LinkedIn: {e}")
            return {}
        
    def transform(self, data: dict) -> dict:
        pass