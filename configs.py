import os
from dotenv import load_dotenv

load_dotenv(override=True)

class MongoConfig:
    MONGO_USER = os.environ["MONGO_USER"]
    MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:27017"


class S3Config:
    S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
    S3_SECRET_KEY = os.environ["S3_SECRET_KEY"]
    
