import pytest
from unittest.mock import MagicMock
from database.mongodb_connector import init


@pytest.mark.asyncio
async def test_init():
    # Mock the AsyncIOMotorClient
    client_mock = MagicMock()

    # Mock the init_beanie function
    init_beanie_mock = MagicMock()

    # Call the init function with the mocked objects
    await init(database="test_db", document_models=["Model1", "Model2"])

    # Assert that the AsyncIOMotorClient is called with the correct arguments
    client_mock.assert_called_once_with("mongodb://localhost:27017")

    # Assert that the init_beanie function is called with the correct arguments
    init_beanie_mock.assert_called_once_with(
        database=client_mock["test_db"], document_models=["Model1", "Model2"]
    )
