import asyncio
from beanie import init_beanie, Document, View
from dotenv import load_dotenv
from typing import Type, Sequence, Optional, List, Union
from .models.lead import Lead
from motor.motor_asyncio import AsyncIOMotorClient
from configs import MongoConfig

load_dotenv()


async def init(
    database: str,
    document_models: Optional[List[Union[Type[Document], Type["View"], str]]],
) -> None:
    # Create Motor client
    client = AsyncIOMotorClient(MongoConfig.MONGO_URI)

    # Initialize beanie with the Lead document class and a database
    await init_beanie(database=client[database], document_models=document_models)

    # Test insert
    lead = Lead(first_name="Mike", last_name="Doe", email="abc@gmail.com")
    await lead.insert()

if __name__ == "__main__":
    asyncio.run(init(database="prospects", document_models=[Lead]))

