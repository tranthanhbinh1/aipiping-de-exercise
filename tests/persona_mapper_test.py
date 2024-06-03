import unittest
from unittest.mock import patch, MagicMock
from database.models.persona import Persona
from database.models.linkedin_data import Linkedin
from database.models.lead import Lead
from persona_mapping.persona_mapper import PersonaMapper


class PersonaMapperTestCase(unittest.TestCase):
    def setUp(self):
        self.persona_mapper = PersonaMapper()

    @patch.object(PersonaMapper, "init")
    async def test_create(self, mock_init):
        mock_init.return_value = None
        persona_mapper = await PersonaMapper.create()
        self.assertIsInstance(persona_mapper, PersonaMapper)
        mock_init.assert_awaited_once()

    @patch.object(PersonaMapper, "init")
    async def test_init(self, mock_init):
        mock_init.return_value = None
        await self.persona_mapper.init()
        mock_init.assert_awaited_once_with(
            database="prospects", document_models=[Lead, Linkedin, Persona]
        )

    @patch.object(Lead, "find_one")
    async def test_query_linkedin_id_found(self, mock_find_one):
        mock_find_one.return_value = MagicMock(linkedin_id="123")
        lead_id = "lead_id"
        result = await self.persona_mapper.query_linkedin_id(lead_id)
        self.assertEqual(result, "123")
        mock_find_one.assert_awaited_once_with(Lead.id == lead_id)

    @patch.object(Lead, "find_one")
    async def test_query_linkedin_id_not_found(self, mock_find_one):
        mock_find_one.return_value = None
        lead_id = "lead_id"
        result = await self.persona_mapper.query_linkedin_id(lead_id)
        self.assertIsNone(result)
        mock_find_one.assert_awaited_once_with(Lead.id == lead_id)

    @patch.object(Linkedin, "find")
    async def test_query_persona_features_found(self, mock_find):
        mock_aggregate = MagicMock()
        mock_aggregate.to_list.return_value = [
            {"company_size": 100, "field_of_study": "Computer Science"}
        ]
        mock_find.return_value = mock_aggregate
        linkedin_id = "linkedin_id"
        result = await self.persona_mapper.query_persona_features(linkedin_id)
        self.assertEqual(
            result, {"company_size": 100, "field_of_study": "Computer Science"}
        )
        mock_find.assert_awaited_once_with(
            {"person.linkedInIdentifier": f"{linkedin_id}"}
        )
        mock_aggregate.aggregate.assert_called_once_with(
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

    @patch.object(Linkedin, "find")
    async def test_query_persona_features_not_found(self, mock_find):
        mock_aggregate = MagicMock()
        mock_aggregate.to_list.return_value = []
        mock_find.return_value = mock_aggregate
        linkedin_id = "linkedin_id"
        result = await self.persona_mapper.query_persona_features(linkedin_id)
        self.assertIsNone(result)
        mock_find.assert_awaited_once_with(
            {"person.linkedInIdentifier": f"{linkedin_id}"}
        )
        mock_aggregate.aggregate.assert_called_once_with(
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

    def test_company_mapper_startup(self):
        company_size = 30
        result = self.persona_mapper.company_mapper(company_size)
        self.assertEqual(result, "startup")

    def test_company_mapper_mid_market(self):
        company_size = 500
        result = self.persona_mapper.company_mapper(company_size)
        self.assertEqual(result, "mid_market")

    def test_company_mapper_multi_national(self):
        company_size = 5000
        result = self.persona_mapper.company_mapper(company_size)
        self.assertEqual(result, "multi_national")

    def test_field_of_study_mapper_found(self):
        field_of_study = "computer science"
        result = self.persona_mapper.fied_of_study_mapper(field_of_study)
        self.assertEqual(result, "computer science")

    def test_field_of_study_mapper_not_found(self):
        field_of_study = "physics"
        result = self.persona_mapper.fied_of_study_mapper(field_of_study)
        self.assertEqual(result, "Other")

    @patch.object(Persona, "insert")
    async def test_insert_persona(self, mock_insert):
        mock_insert.return_value = None
        company_type = "startup"
        academic_field = "computer science"
        await self.persona_mapper.insert_persona(company_type, academic_field)
        mock_insert.assert_awaited_once_with(
            company_type=company_type,
            academic_field=academic_field,
        )


if __name__ == "__main__":
    unittest.main()
