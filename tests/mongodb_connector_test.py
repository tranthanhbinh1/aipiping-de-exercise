import pytest
from database.models.lead import Lead
from database.models.linkedin_data import Linkedin
from database.models.persona import Persona
from database.mongodb_connector import init
from unittest.mock import patch, MagicMock


@pytest.mark.asyncio
async def test_init():
    with patch(
        "motor.motor_asyncio.AsyncIOMotorClient", return_value=MagicMock()
    ) as mock:
        # Call the function that should use AsyncIOMotorClient
        await init(database="prospects", document_models=[Lead, Linkedin, Persona])

        # Assert that AsyncIOMotorClient was called
        mock.assert_called_once()
