from beanie import Document
from pydantic import Field, BaseModel
from typing import Optional
from uuid import uuid4


class Linkedin(Document):
    id: str = Field(default_factory=lambda: uuid4().hex)
    credits_left: Optional[int] = None
    person: Optional[dict] = None
    company: Optional[dict] = None
    rate_limit_left: Optional[int] = None
    success: Optional[bool] = None

    class Settings:
        name = "linkedin_raw_data"


class PersonaFeaturesView(BaseModel):
    person: Optional[dict] = None
    company: Optional[dict] = None
    
    
    # class Settings:
    #     projection = {
    #         "credits_left": 0,
    #         "field_of_study": {"$person.schools.educationHistory"},
    #         "company_size": "$company.employeeCount",
    #         "rate_limit_left": 0,
    #         "success": 0,
    #     }
