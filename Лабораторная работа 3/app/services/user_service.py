from typing import List
from repositories.user_repository import UserRepository
from orm.main import User
from schemas.user_schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: int):
        return await self.user_repository.get_by_id(user_id)

    async def get_by_filter(self, count: int = 10, page: int = 1, **kwargs) -> List[User]:
        return await self.user_repository.get_by_filter(count, page, **kwargs)

    async def create(self, user_data: UserCreate) -> User:
        return await self.user_repository.create(user_data)

    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        return await self.user_repository.update(user_id, user_data)

    async def delete(self, user_id: int) -> None:
        return await self.user_repository.delete(user_id)
    
    async def get_total_count(self, **kwargs) -> int:
        return await self.user_repository.get_total_count(**kwargs)
