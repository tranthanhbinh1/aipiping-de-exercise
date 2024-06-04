import pandas as pd
import logging
import asyncio
from typing import Literal
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
        await init(database="prospects", document_models=[Lead, Linkedin, Persona])

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

    @staticmethod
    def company_mapper(
        company_size: int,
    ) -> Literal["startup", "mid_market", "multi_national"]:
        """
        Maps the company size to a company category.

        Args:
            company_size (int): The size of the company.

        Returns:
            str: The category of the company.
        """
        if company_size < 50:
            return "startup"
        elif 50 < company_size < 1000:
            return "mid_market"
        else:
            return "multi_national"

    @classmethod
    def fied_of_study_mapper(cls, field_of_study: str) -> str:
        """
        Maps the field of study to a field category.

        Args:
            field_of_study (str): The field of study.

        Returns:
            str: The category of the field of study.
        """
        field_of_study = field_of_study.lower()
        for index, row in cls.academic_df.iterrows():
            if field_of_study in row["field_of_study"].lower():
                return row["academic_field"]
        return "Other"

    async def insert_persona(
        self,
        lead_id: str,
        company_type: Literal["startup", "mid_market", "multi_national"],
        academic_field: str,
    ) -> None:
        """
        Inserts the persona features into the database.

        Args:
            lead_id (str): The ID of the lead.
            persona_features (dict): The persona features of the lead.

        Returns:
            None
        """
        persona = Persona(
            company_type=company_type,
            academic_field=academic_field,
            lead_ids=[lead_id],
        )
        await persona.insert()
        logging.info("Persona inserted successfully!")


if __name__ == "__main__":

    async def main(lead_id: str):
        persona_mapper = await PersonaMapper.create()
        linkedin_id = await persona_mapper.query_linkedin_id(lead_id)
        logging.info("Linkedin_id: %s", linkedin_id)
        if linkedin_id:
            persona_features = await persona_mapper.query_persona_features(linkedin_id)
        if persona_features:
            company_type = persona_mapper.company_mapper(
                persona_features["company_size"]
            )
            logging.info("Company type: %s", company_type)
            academic_field = persona_mapper.fied_of_study_mapper(
                persona_features["field_of_study"]
            )
            logging.info("Academic field: %s", academic_field)

            await persona_mapper.insert_persona(lead_id, company_type, academic_field)

    asyncio.run(main(lead_id="dd4483e4748c4277b1f989358dc51408"))

