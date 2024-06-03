import pytest
from database.models.lead import Lead
from database.models.linkedin_data import Linkedin
from database.models.persona import Persona
from database.mongodb_connector import init
from configs import MongoConfig
from unittest.mock import patch, MagicMock, AsyncMock


@pytest.mark.asyncio
async def test_init_success(mocker):
    # Mock MongoDB client and init_beanie
    mock_client = mocker.patch(
        "motor.motor_asyncio.AsyncIOMotorClient", new=AsyncMock()
    )
    mock_init_beanie = mocker.patch("beanie.init_beanie")
    mock_db = AsyncMock()
    mock_client.return_value.__getitem__.return_value = mock_db

    # Call the function
    await init("prospects", [Lead, Linkedin])

    # Assertions
    mock_client.assert_called_once_with(MongoConfig.MONGO_URI)
    mock_client.return_value.__getitem__.assert_called_once_with("prospects")
    mock_init_beanie.assert_called_once_with(
        database=mock_db, document_models=[Lead, Linkedin]
    )


@pytest.mark.asyncio
async def test_init_failure(mocker):
    # Mock MongoDB client to raise an exception
    mock_client = mocker.patch(
        "motor.motor_asyncio.AsyncIOMotorClient", new=AsyncMock()
    )
    mock_client.side_effect = Exception("Connection Error")

    # Call the function and expect an exception
    with pytest.raises(Exception):
        await init("prospects", [Lead, Linkedin])
