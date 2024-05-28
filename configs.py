import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:27017"