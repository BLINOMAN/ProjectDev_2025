
from typing import List, Optional
from app.orm.main import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: str) -> Optional[User]:        
        return await self.user_repository.get_by_id(user_id)

    async def get_by_filter(self, count: int = 10, page: int = 1, **kwargs) -> List[User]:
        return await self.user_repository.get_by_filter(count, page, **kwargs)

    async def create(self, user_data: UserCreate) -> User:
        existing_users = await self.user_repository.get_by_filter(email=user_data.email)
        if existing_users:
            raise ValueError(f"User with email {user_data.email} already exists")

        return await self.user_repository.create(user_data)

    async def update(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        existing_user = await self.get_by_id(user_id)
        if not existing_user:
            return None

        if user_data.email and user_data.email != existing_user.email:
            user_with_email = await self.user_repository.get_by_filter(email=user_data.email)
            if user_with_email:
                raise ValueError(f"User with email {user_data.email} already exists")

        return await self.user_repository.update(user_id, user_data)

    async def delete(self, user_id: str) -> bool:
        return await self.user_repository.delete(user_id)

    async def get_total_count(self, **kwargs) -> int:
        return await self.user_repository.get_total_count(**kwargs)