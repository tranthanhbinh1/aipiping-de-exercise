import unittest
from unittest.mock import patch, MagicMock
from database.models.lead import Lead, LeadView
from database.models.linkedin_data import Linkedin
from database.s3_connector import S3Connector
from database.mongodb_connector import init
from utils.logging_config import setup_logging
from data_pipeline.elt_process import ELT


class ELTTestCase(unittest.TestCase):
    def setUp(self):
        setup_logging()
        self.elt = ELT(email="test@example.com")

    @patch("requests.get")
    def test_extract_success(self, mock_get):
        mock_get.return_value = MagicMock(json=lambda: {"data": "extracted_data"})
        data = self.elt.extract()
        self.assertEqual(data, {"data": "extracted_data"})

    @patch("requests.get")
    def test_extract_failure(self, mock_get):
        mock_get.side_effect = Exception("Failed to extract data")
        data = self.elt.extract()
        self.assertEqual(data, {})

    @patch.object(S3Connector, "put_object")
    def test_load_s3(self, mock_put_object):
        self.elt.data = {"data": "extracted_data"}
        self.elt.load_s3()
        mock_put_object.assert_called_once_with(
            bucket="linkedin_bucket", key="raw.json", body=b'{"data": "extracted_data"}'
        )

    @patch.object(init, "init")
    async def test_async_load_mongo_raw(self, mock_init):
        self.elt.data = {
            "credits_left": 10,
            "person": "John Doe",
            "rate_limit_left": 100,
            "success": True,
        }
        await self.elt.async_load_mongo_raw()
        mock_init.assert_called_once_with(
            database="mongodb_db_name", document_models=[Linkedin]
        )
        Linkedin.insert.assert_called_once_with(
            credits_left=10,
            person="John Doe",
            rate_limit_left=100,
            success=True,
        )

    @patch.object(init, "init")
    async def test_transform(self, mock_init):
        mock_find = MagicMock()
        mock_find.sort.return_value.project.return_value.limit.return_value.to_list.return_value = [
            Lead(
                linkedin_id="123",
                status="active",
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                photo_url="http://example.com/photo.jpg",
            )
        ]
        Linkedin.find.return_value = mock_find
        await self.elt.transform()
        mock_init.assert_called_once_with(
            database="mongodb_db_name", document_models=[Linkedin, Lead]
        )
        mock_find.sort.assert_called_once_with("-_id")
        mock_find.sort.return_value.project.assert_called_once_with(LeadView)
        mock_find.sort.return_value.project.return_value.limit.assert_called_once_with(
            1
        )
        self.assertEqual(self.elt.doc.linkedin_id, "123")
        self.assertEqual(self.elt.doc.status, "active")
        self.assertEqual(self.elt.doc.first_name, "John")
        self.assertEqual(self.elt.doc.last_name, "Doe")
        self.assertEqual(self.elt.doc.email, "john.doe@example.com")
        self.assertEqual(self.elt.doc.photo_url, "http://example.com/photo.jpg")

    @patch.object(init, "init")
    async def test_load_mongo_transformed(self, mock_init):
        self.elt.doc = Lead(
            linkedin_id="123",
            status="active",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            photo_url="http://example.com/photo.jpg",
        )
        await self.elt.load_mongo_transformed()
        mock_init.assert_called_once_with(
            database="mongodb_db_name", document_models=[Lead]
        )
        self.elt.doc.insert.assert_called_once()

    @patch.object(ELT, "async_load_mongo_raw")
    @patch.object(ELT, "transform")
    @patch.object(ELT, "load_mongo_transformed")
    async def test_main(
        self, mock_load_mongo_transformed, mock_transform, mock_async_load_mongo_raw
    ):
        await self.elt.main()
        mock_async_load_mongo_raw.assert_called_once()
        mock_transform.assert_called_once()
        mock_load_mongo_transformed.assert_called_once()


if __name__ == "__main__":
    unittest.main()
