from beanie import Document
from pydantic import Field,BaseModel
from typing import Optional
from uuid import uuid4


class Lead(Document):
    id: str = Field(default_factory=lambda: uuid4().hex)
    linkedin_id: Optional[str] = None
    status: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None

    class Settings:
        name = "leads"


class LeadView(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    linkedin_id: Optional[str] = None
    status: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None

    class Settings:
        projection = {
            "linkedin_id": "$person.linkedInIdentifier",
            "last_name": "$person.lastName",
            "first_name": "$person.firstName",
            "emails": "$person.email",
            "photo_url": "$person.photoUrl",
        }
