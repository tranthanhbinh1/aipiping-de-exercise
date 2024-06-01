from beanie import Document
from pydantic import BaseModel
from pydantic import Field
from typing import Optional
from uuid import uuid4


class Lead(Document):
    id: str = Field(default_factory=lambda: uuid4().hex)
    status: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None

    class Settings:
        name = "leads"


class LeadView(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    status: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None

    class Settings:
        projection = {
            "last_name": "$person.lastName",
            "first_name": "$person.firstName",
            "emails": "$person.email",
            "photo_url": "$person.photoUrl",
        }
