import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm.main import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate, UserUpdate


@pytest.mark.asyncio
async def test_create_user(user_repository: UserRepository, test_db_session: AsyncSession):
    user_data = UserCreate(username="Test User", email="test@example.com")
    user = await user_repository.create(user_data)  
    assert user.username == "Test User"
    assert user.email == "test@example.com"
    assert user.id is not None

    result = await test_db_session.execute(select(User).where(User.id == user.id))
    saved_user = result.scalar_one_or_none()
    assert saved_user is not None
    assert saved_user.username == "Test User"


@pytest.mark.asyncio
async def test_get_user_by_id(user_repository: UserRepository, test_db_session: AsyncSession):
    user_data = UserCreate(username="Test User", email="test@example.com")
    created_user = await user_repository.create(user_data)  
    await test_db_session.commit()

    user = await user_repository.get_by_id(created_user.id)  

    assert user is not None
    assert user.username == "Test User"


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_repository: UserRepository, test_db_session: AsyncSession):
    user = await user_repository.get_by_id("nonexistent-id")  
    assert user is None


@pytest.mark.asyncio
async def test_update_user(user_repository: UserRepository, test_db_session: AsyncSession):
    user_data = UserCreate(username="Original Name", email="original@example.com")
    created_user = await user_repository.create(user_data)  
    await test_db_session.commit()

    update_data = UserUpdate(username="Updated Name")
    updated_user = await user_repository.update(created_user.id, update_data)  

    assert updated_user is not None
    assert updated_user.username == "Updated Name"
    assert updated_user.email == "original@example.com"  


@pytest.mark.asyncio
async def test_delete_user(user_repository: UserRepository, test_db_session: AsyncSession):
    user_data = UserCreate(username="To Delete", email="delete@example.com")
    created_user = await user_repository.create(user_data)  
    await test_db_session.commit()

    result = await user_repository.delete(created_user.id)  

    assert result is True

    result = await test_db_session.execute(select(User).where(User.id == created_user.id))
    deleted_user = result.scalar_one_or_none()
    assert deleted_user is None


@pytest.mark.asyncio
async def test_get_all_users(user_repository: UserRepository, test_db_session: AsyncSession):    
    users_data = [
        UserCreate(username="User 1", email="user1@example.com"),
        UserCreate(username="User 2", email="user2@example.com"),
    ]
    for data in users_data:
        await user_repository.create(data)  
    await test_db_session.commit()

    users = await user_repository.get_by_filter(count=10, page=1)  
    assert len(users) == 2
    assert users[0].username == "User 1"
    assert users[1].username == "User 2"