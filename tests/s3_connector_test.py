from moto import mock_aws
from database.s3_connector import S3Connector
import pytest


@pytest.fixture
def s3_connector():
    with mock_aws():
        yield S3Connector()


@mock_aws
def test_put_object(s3_connector):
    s3_connector.s3.create_bucket(Bucket="linkedin-data")

    result = s3_connector.put_object("linkedin-data", "test-key", "test body")

    # Assert the success of the upload by checking if a specific response key exists
    assert "ETag" in result

    # Retrieve the uploaded object to verify its contents
    obj = s3_connector.s3.get_object(Bucket="linkedin-data", Key="test-key")
    assert obj["Body"].read().decode("utf-8") == "test body"


@mock_aws
def test_get_object(s3_connector):
    s3_connector.s3.create_bucket(Bucket="linkedin-data")

    s3_connector.put_object("linkedin-data", "test-key", "test body")

    # Test the get_object method
    obj = s3_connector.get_object("linkedin-data", "test-key")

    # Check if obj is not none and is a dictionary
    assert obj and isinstance(obj, dict)

    # Assert that the body of the object matches the expected content
    assert obj.get("Body") is not None
    assert obj["Body"].read().decode("utf-8") == "test body"
