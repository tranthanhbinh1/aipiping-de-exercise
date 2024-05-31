import asyncio
from mongodb_connector import init
from beanie import init_beanie, Document, View
from .models.lead import Lead
from .models.linkedin_data import Linkedin
# from motor.motor_asyncio import AsyncIOMotorClient
# from configs import MongoConfig


if __name__ == "__main__":
    asyncio.run(init(database="prospects", document_models=[Lead, Linkedin]))
    
#TODO: 1 database for both Lead and Linkedin data or 1 for Lead and 1 for Linkedin data?