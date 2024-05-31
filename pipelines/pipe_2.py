import requests
import logging
from database import s3_connector
from utils.logging_config import setup_logging  

setup_logging() 

class ELT:
    def __init__(self) -> None:
        self.s3_connector = s3_connector.S3Connector()
        self.linkedin_api = "http://127.0.0.1:8000/get_linkedin_data/abc@gmail.com"
        self.data: dict = None
        
    def extract(self) -> dict:
        try:
            data = requests.get(self.linkedin_api)
            logging.info("Extracted data from LinkedIn")
            return data.json()
        except Exception as e:
            logging.error(f"Failed to extract data from LinkedIn: {e}")
            return {}
    
    def load(self) -> None:
        
        pass
    
    def transform(self, data: dict) -> dict:
        pass
    
    
    
if __name__ == "__main__":
    elt = ELT()
    data = elt.extract()
    logging.info(data)