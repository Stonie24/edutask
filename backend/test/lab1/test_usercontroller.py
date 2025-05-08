import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController
from src.util.dao import DAO

@pytest.fixture
def mock_dao():
    return MagicMock(spec=DAO)

@pytest.fixture
def controller(mock_dao):
    return UserController(dao=mock_dao)

@pytest.mark.usercontroller
class TestGetUserByEmail:

    def test_valid_email_one_user_returns_user(self, controller, mock_dao):
        mock_user = {'email': 'user@email.com'}
        mock_dao.find.return_value = [mock_user]
        result = controller.get_user_by_email("user@email.com")
        assert result == mock_user

    def test_valid_email_one_user_calls_dao(self, controller, mock_dao):
        mock_user = {'email': 'user@email.com'}
        mock_dao.find.return_value = [mock_user]
        controller.get_user_by_email("user@email.com")
        mock_dao.find.assert_called_once_with({'email': 'user@email.com'})

    def test_invalid_email_raises_value_error(self, controller, mock_dao):
        mock_dao.find.side_effect = ValueError("Error: invalid email address")
        with pytest.raises(ValueError) as exc:
            controller.get_user_by_email("user")

    def test_valid_email_multiple_users_prints_warning(self, controller, mock_dao, capsys):
        users = [{'email': 'user@email.com'}, {'email': 'user@email.com'}]
        mock_dao.find.return_value = users
        controller.get_user_by_email("user@email.com")
        captured = capsys.readouterr()
        assert "more than one user found" in captured.out

    def test_valid_email_multiple_users_returns_first_user(self, controller, mock_dao):
        users = [{'email': 'user@email.com'}, {'email': 'user@email.com'}]
        mock_dao.find.return_value = users
        result = controller.get_user_by_email("user@email.com")
        assert result == users[0]

    def test_valid_email_no_users_found_returns_none(self, controller, mock_dao):
        mock_dao.find.return_value = []
        result = controller.get_user_by_email("user@email.com")
        assert result is None

    def test_trigger_exception_from_db(self, controller, mock_dao):
        mock_dao.find.side_effect = Exception("DB Failure")
        with pytest.raises(Exception) as exc:
            controller.get_user_by_email("user@email.com")
