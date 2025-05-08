import pytest
from unittest.mock import patch

from pymongo.errors import WriteError

from src.util.dao import DAO

jsonData = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["description", "done"],
        "properties": {
            "description": {
                "bsonType": "string",
                "uniqueItems": True
            },
            "done": {
                "bsonType": "bool"
            }
        }
    }
}

@pytest.fixture
def sut():
    with patch("src.util.dao.getValidator", autospec=True) as mockedgetvalidator:
        mockedgetvalidator.return_value = jsonData
        sut = DAO(collection_name="test")
    
    yield sut
    sut.collection.drop()

@pytest.mark.daocreate
class TestCreateMethodInDAO:

    def test_with_valid_data(self, sut):
        data = {
            "description": "a description",
            "done": True
        }

        result = sut.create(data)

        assert "_id" in result
        assert result["description"] == "a description"
        assert result["done"] == True

    def test_without_one_parameter_field(self, sut):
        data = {
            "description": "a description",
        }

        with pytest.raises(WriteError):
            sut.create(data)

    def test_invalid_data_type(self, sut):
        data = {
            "description": "a description",
            "done": 123123
        }

        with pytest.raises(WriteError):
            sut.create(data)

    def test_empty_dict(self, sut):
        data = {}

        with pytest.raises(WriteError):
            sut.create(data)

    @pytest.mark.parametrize("desc1,desc2", [
        ("a description", "a description"),
    ])
    def test_value_flagged_as_unique(self, sut, desc1, desc2):
        data1 = {
            "description": desc1,
            "done": True
        }

        data2 = {
            "description": desc2,
            "done": True
        }

        sut.create(data1)
        with pytest.raises(WriteError):
            sut.create(data2)
