from beanie import Document
from pydantic import Field
from typing import Optional
from uuid import uuid4


class Linkedin(Document):
    id: str = Field(default_factory=lambda: uuid4().hex)
    credits_left: Optional[int] = None
    person: Optional[dict]  = None
    rate_limit_left: Optional[int] = None
    success: Optional[bool] = None