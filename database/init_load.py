import asyncio
from beanie import init_beanie
from dotenv import load_dotenv
from .models.leads import Lead
from motor.motor_asyncio import AsyncIOMotorClient
from configs import MONGO_URI

load_dotenv()


async def init():
    # Create Motor client
    client = AsyncIOMotorClient(MONGO_URI)

    # Initialize beanie with the Lead document class and a database
    await init_beanie(database=client.prospects, document_models=[Lead])


if __name__ == "__main__":
    import asyncio

    asyncio.run(init())
