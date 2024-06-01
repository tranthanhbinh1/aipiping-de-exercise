import asyncio
import logging
from utils.logging_config import setup_logging
from .mongodb_connector import init
from .models.lead import Lead
from .models.linkedin_data import Linkedin
from data_pipeline.elt_process import ELT
from configs import MONGODB_DB_NAME

setup_logging()


async def init_load():
    await init(database=MONGODB_DB_NAME, document_models=[Lead, Linkedin])
    logging.info("Successfully initilized database!")

    # Test insert
    lead = Lead(first_name="Mike", last_name="Doe", email="abc@gmail.com")
    await lead.insert()

    data = ELT.extract()

    linkedin = Linkedin(
        credits_left=data["credits_left"],
        person=data["person"],
        rate_limit_left=data["rate_limit_left"],
        success=data["success"],
    )
    
    await linkedin.insert()


if __name__ == "__main__":
    asyncio.run(init_load())
    
    logging.info("Successfullly initialized load!")

