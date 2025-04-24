# import pytest
# from unittest.mock import MagicMock

# from bson.objectid import ObjectId
# from pymongo.errors import WriteError

# from src.util.dao import DAO

# @pytest.fixture
# def mock_collection():
#     return MagicMock()


# @pytest.fixture
# def dao(mock_collection):
#     dao = DAO.__new__(DAO)  # bypass __init__
#     dao.collection = mock_collection
#     return dao


# @pytest.mark.daocreate
# class TestCreateMethodInDAO:
        
#     def test_with_valid_data(self, dao, mock_collection):
#         test_data  = { "name": "Test User", "active": True }
#         fake_id = ObjectId()
#         expected_obj = {**test_data, "_id": fake_id}

#         mock_collection.insert_one.return_value.inserted_id = fake_id
#         mock_collection.find_one.return_value = expected_obj

#         result = dao.create(test_data)

#         mock_collection.insert_one.assert_called_once_with(test_data)
#         mock_collection.find_one.assert_called_once_with({'_id': fake_id})
#         assert result["_id"]["$oid"] == str(fake_id)
#         assert result["name"] == "Test User"
#         assert result["active"] == True
 
#     def test_without_one_required_field(self, dao, mock_collection):
#         data = {"active": True }
    
#         def side_effect(document):
#             if "name" in document and "active" in document:
#                 pass
#             else:
#                 raise WriteError("Insertion Failed: missing required field 'name'", code=121)
#             return MagicMock(inserted_id=ObjectId())
            
#         mock_collection.insert_one.side_effect = side_effect

#         with pytest.raises(WriteError) as exc_info:
#             dao.create(data)
        
#         assert "Insertion Failed" in str(exc_info.value)

#     def test_invalid_data_type(self, dao, mock_collection):
#         data = { "name": 1234, "active": True }
#         def side_effect(document):
#             if (isinstance(document.get('name'), str) and isinstance(document.get('active'), bool)) :
#                 pass
#             else:
#                 raise WriteError("Insertion Failed: missing required fields", code=121)
#             return MagicMock(inserted_id=ObjectId())
            
#         mock_collection.insert_one.side_effect = side_effect

#         with pytest.raises(WriteError) as exc_info:
#             dao.create(data)
        
#         assert "Insertion Failed" in str(exc_info.value)

#     def test_empty_dict(self, dao, mock_collection):
#         data = {}

#         def side_effect(document):
#             if "name" in document and "active" in document:
#                 pass
#             else:
#                 raise WriteError("Insertion Failed: missing required field 'name'", code=121)
#             return MagicMock(inserted_id=ObjectId())
            
#         mock_collection.insert_one.side_effect = side_effect

#         with pytest.raises(WriteError) as exc_info:
#             dao.create(data)
        
#         assert "Insertion Failed" in str(exc_info.value)

#     def test_value_flagged_as_unique(self, dao, mock_collection):
#         data_one = { "name": "Test User", "active": True }
#         data_two = { "name": "Test User", "active": False }

#         fake_id = ObjectId()
#         expected_obj = {
#             "name": "Test User",
#             "active": True,
#             "_id": { "$oid": str(fake_id) }
#         }

#         inserted_names = set() 

#         def side_effect(document):
#             if document["name"] in inserted_names:
#                 raise WriteError("Duplicate key error", code=11000)
#             inserted_names.add(document["name"])
#             return MagicMock(inserted_id=fake_id)
        
#         mock_collection.insert_one.side_effect = side_effect
#         mock_collection.find_one.return_value = expected_obj

#         result = dao.create(data_one)

#         mock_collection.insert_one.assert_called_with(data_one)
#         mock_collection.find_one.assert_called_with({ "_id": fake_id })
#         assert result["_id"] == expected_obj["_id"]
#         assert result["name"] == expected_obj["name"]
#         assert result["active"] == expected_obj["active"]

#         with pytest.raises(WriteError) as exc_info:
#             dao.create(data_two)

#         assert "Duplicate key error" in str(exc_info.value)


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

    def test_value_flagged_as_unique(self, sut):
        data1 = {
            "description": "a description",
            "done": True,
            "uniqueItems": True
        }

        data2 = {
            "description": "a description",
            "done": True,
            "uniqueItems": True
        }

        with pytest.raises(WriteError):
            sut.create(data1)
            sut.create(data2)
