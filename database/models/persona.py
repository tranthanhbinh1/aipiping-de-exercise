from beanie import Document
from pydantic import Field
from typing import Optional, Literal
from uuid import uuid4


class Persona(Document):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: Optional[str] = None
    academic_field: Optional[str] = None
    company_type: Optional[
        Literal["startup", "mid_market", "multi_national"]
    ] = None
    lead_ids: Optional[list[str]] = None
    
    class Settings:
        name = "personas"
