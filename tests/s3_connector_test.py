import pytest
from unittest.mock import MagicMock
from database.s3_connector import S3Connector

@pytest.fixture
def s3_connector():
    return S3Connector()

def test_get_object(s3_connector):
    # Mock the boto3 client's get_object method
    s3_connector.s3.get_object = MagicMock(return_value={"Body": "test body"})
    
    # Call the get_object method and assert the result
    result = s3_connector.get_object("linkedin-data", "test-key")
    assert result == {"Body": "test body"}
    s3_connector.s3.get_object.assert_called_once_with(Bucket="linkedin-data", Key="test-key")

def test_put_object(s3_connector):
    # Mock the boto3 client's put_object method
    s3_connector.s3.put_object = MagicMock()
    
    # Call the put_object method and assert the result
    result = s3_connector.put_object("linkedin-data", "test-key", "test body")
    assert result is None
    s3_connector.s3.put_object.assert_called_once_with(Bucket="linkedin-data", Key="test-key", Body="test body")