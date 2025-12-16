import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm.main import User
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user_schemas import UserCreate, UserUpdate


@pytest.mark.asyncio
async def test_user_service_create():
    mock_repo = AsyncMock(spec=UserRepository)
    
    user_service = UserService(mock_repo)    
    user_data = UserCreate(username="Test User", email="test@example.com")
    
    mock_repo.get_by_filter.return_value = []
    
    mock_user = User(id="123", username="Test User", email="test@example.com")
    mock_repo.create.return_value = mock_user

    result = await user_service.create(user_data)
    mock_repo.create.assert_called_once_with(user_data)  
    
    assert result.username == "Test User"


@pytest.mark.asyncio
async def test_user_service_get_by_id():
    mock_repo = AsyncMock(spec=UserRepository)
    user_service = UserService(mock_repo)

    mock_user = User(id="123", username="Test User", email="test@example.com")
    mock_repo.get_by_id.return_value = mock_user

    result = await user_service.get_by_id("123")

    mock_repo.get_by_id.assert_called_once_with("123")  
    assert result.id == "123"


@pytest.mark.asyncio
async def test_user_service_get_by_id_not_found():
    mock_repo = AsyncMock(spec=UserRepository)
    user_service = UserService(mock_repo)

    mock_repo.get_by_id.return_value = None

    result = await user_service.get_by_id("nonexistent")

    mock_repo.get_by_id.assert_called_once_with("nonexistent") 
    assert result is None


@pytest.mark.asyncio
async def test_user_service_update():
    mock_repo = AsyncMock(spec=UserRepository)
    user_service = UserService(mock_repo)

    existing_user = User(id="123", username="Old Name", email="old@example.com")
    mock_repo.get_by_id.return_value = existing_user

    update_data = UserUpdate(username="New Name")
    updated_user = User(id="123", username="New Name", email="old@example.com")
    mock_repo.update.return_value = updated_user

    result = await user_service.update("123", update_data)

    mock_repo.update.assert_called_once_with("123", update_data)  
    assert result.username == "New Name"


@pytest.mark.asyncio
async def test_user_service_delete():
    mock_repo = AsyncMock(spec=UserRepository)
    user_service = UserService(mock_repo)

    mock_repo.delete.return_value = True

    result = await user_service.delete("123")

    mock_repo.delete.assert_called_once_with("123") 
    assert result is True