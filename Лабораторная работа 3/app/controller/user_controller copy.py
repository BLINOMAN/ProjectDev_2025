from typing import List
from services.user_service import UserService
from schemas.user_schemas import UserResponse, UserCreate, UserUpdate
from litestar import Controller, get, post, put, delete
from litestar.params import Parameter
from litestar.di import Provide
from litestar.exceptions import NotFoundException


class UserController(Controller):
    path = "/users"

    @get("/get_user/{user_id:uuid}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: int = Parameter(gt=0),
    ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get("/get_all_users")
    async def get_all_users(
        self,
        user_service: UserService,
        count: int = Parameter(ge=1, le=100, default=10),
        page: int = Parameter(ge=1, default=1)
    ) -> List[UserResponse]:
        print('get_all_users')
        result = await user_service.get_by_filter(count=count, page=page)
        results = [UserResponse.model_validate(user) for user in result]
        return results
        

    @post("/create_user")
    async def create_user(
        self,
        user_service: UserService,
        user_data: UserCreate,
    ) -> UserResponse:
        result = await user_service.create(user_data=user_data)
        return UserResponse.model_validate(result)

    @delete("/delete/{user_id:int}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: int,
    ) -> None:
        result = await user_service.delete(user_id=user_id)
        if not result:
            raise NotFoundException(detail=f"User with ID {user_id} not found")

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: int,
        user_data: UserUpdate,
    ) -> UserResponse:
        result = await user_service.update(user_id=user_id, user_data=user_data)
        if not result:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(result)