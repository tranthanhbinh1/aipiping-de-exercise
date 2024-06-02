import pandas as pd
import logging
import asyncio
from typing import Optional
from database.mongodb_connector import init
from database.models.persona import Persona
from database.models.linkedin_data import Linkedin
from database.models.lead import Lead
from utils.logging_config import setup_logging

setup_logging()


class PersonaMapper:
    """
    A class that maps personas to LinkedIn profiles.

    Attributes:
        academic_df (pd.DataFrame): A DataFrame containing academic data.

    Methods:
        create: A class method that creates an instance of PersonaMapper.
        init: An asynchronous method that initializes the PersonaMapper instance.
        query_linkedin_id: An asynchronous method that queries the LinkedIn ID for a given lead ID.
        query_persona_features: An asynchronous method that queries the persona features for a given LinkedIn ID.
    """

    academic_df: pd.DataFrame = pd.read_csv("test_data/fields_data_transformed.csv")

    @classmethod
    async def create(cls):
        self = PersonaMapper()
        await self.init()
        return self

    async def init(self):
        await init(database="prospects", document_models=[Lead, Linkedin])

    async def query_linkedin_id(self, lead_id: str) -> str | None:
        """
        Queries the LinkedIn ID for a given lead ID.

        Args:
            lead_id (str): The ID of the lead.

        Returns:
            str | None: The LinkedIn ID of the lead if found, None otherwise.
        """
        lead_result = await Lead.find_one(Lead.id == lead_id)
        if lead_result:
            logging.info("Lead result: %s", lead_result)
            return lead_result.linkedin_id
        else:
            logging.error("No linkedin_id found!")
            return None

    async def query_persona_features(self, linkedin_id: str) -> dict | None:
        """
        Queries the persona features for a given LinkedIn ID.
        Right now, the persona features contains the company size and the field of study.

        Args:
            linkedin_id (str): The LinkedIn ID of the lead.
        Returns:
            dict | None: The persona features of the lead if found, None otherwise.
        """
        logging.info(f"Querying for linkedin identifier:{linkedin_id}")
        persona_features = (
            await Linkedin.find({"person.linkedInIdentifier": f"{linkedin_id}"})
            .aggregate(
                [
                    {"$match": {"person.linkedInIdentifier": f"{linkedin_id}"}},
                    {
                        "$project": {
                            "company_size": "$company.employeeCount",
                            "field_of_study": {
                                "$arrayElemAt": [
                                    "$person.schools.educationHistory.fieldOfStudy",
                                    0,
                                ]
                            },
                        }
                    },
                    {"$sort": {"_id": -1}},
                    {"$limit": 1},
                ]
            )
            .to_list()
        )
        if persona_features:
            logging.info("Linkedin result: %s", persona_features[0])
            return persona_features[0]
        else:
            logging.error("No linkedin data found!")
            return None


if __name__ == "__main__":

    async def main():
        persona_mapper = await PersonaMapper.create()
        linkedin_id = await persona_mapper.query_linkedin_id(
            "dd4483e4748c4277b1f989358dc51408"
        )
        logging.info("Linkedin_id: %s", linkedin_id)
        if linkedin_id:
            await persona_mapper.query_persona_features(linkedin_id)

    asyncio.run(main())

#TODO: MAke the actual mapping, map the field of study and the company size