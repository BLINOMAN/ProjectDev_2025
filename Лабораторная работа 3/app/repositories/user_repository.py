from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from orm.main import User
from schemas.user_schemas import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int):
        result = await self.session.execute(
            select(User).where(User.id==user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_filter(self, count: int = 10, page: int = 1, **kwargs) -> List[User]:
        print('get_by_filter')
        result = await self.session.execute(
            select(User).filter_by(**kwargs).offset((page-1)*count).limit(count)
        )
        print(result)
        return list(result.scalars().all())

    async def create(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            return None

        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await self.session.commit()
        return user

    async def delete(self, user_id: int) -> None:
        user = await self.session.get(User, user_id)
        if not user:
            return None
        await self.session.delete(user)
        await self.session.commit()
        return user
    
    async def get_total_count(self, **kwargs):
        query = select(User)

        if kwargs:
            for key, value in kwargs.items():
                if hasattr(User, key):
                    query = query.where(getattr(User, key) == value)

        result = await self.session.execute(select(User.id))
        return len(result.scalars().all())
