import json
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/get_linkedin_data/{email}")
def get_linkedin_data(email:str) -> dict:
    return json.loads(open("test_data/linkedin_example.json").read())