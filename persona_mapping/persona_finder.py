import logging
import asyncio
from typing import Literal
from database.mongodb_connector import init
from database.models.persona import Persona
from database.models.linkedin_data import Linkedin
from database.models.lead import Lead
from utils.logging_config import setup_logging

setup_logging() 

class LeadFinder:
    """
    A class that finds Leads, given a Persona.

    Attributes:
        lead_id.

    Methods:
        create: A class method that
    """

    @classmethod
    async def create(cls):
        self = LeadFinder()
        await self.init()
        return self

    async def init(self):
        await init(database="prospects", document_models=[Lead, Persona])

    async def query_lead(self, lead_ids: list[str]) -> str | None:
        """
        Queries the Lead for a given Persona.

        Args:
            persona (Persona): The Persona to query.

        Returns:
            str | None: The Lead ID of the Persona if found, None otherwise.
        """
        # leads ids is a list
        lead_ids = await Lead.find(Lead.id in lead_ids)
        if lead_ids:
            logging.info("Lead result: %s", lead_ids)
            return lead_ids
        else:
            logging.error("No lead found!")
            return None
