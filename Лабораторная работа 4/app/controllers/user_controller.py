from litestar import Controller, get, post, put, delete
from litestar.params import Parameter, Body
from litestar.exceptions import NotFoundException, ValidationException
from litestar.status_codes import HTTP_204_NO_CONTENT
from app.services.user_service import UserService
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse


class UserController(Controller):
    path = "/users"

    @get("/{user_id:str}")
    async def get_user_by_id(
            self,
            user_service: UserService,
            user_id: str = Parameter(description="ID пользователя"),
    ) -> UserResponse:
        
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
            self,
            user_service: UserService,
            count: int = Parameter(gt=0, le=100, default=10, description="Количество записей"),
            page: int = Parameter(gt=0, default=1, description="Номер страницы"),
    ) -> dict:
        
        users = await user_service.get_by_filter(count=count, page=page)
        total_count = await user_service.get_total_count()

        return {
            "users": [UserResponse.model_validate(user) for user in users],
            "total_count": total_count,
            "page": page,
            "count": count
        }

    @post('/create_user')
    async def create_user(
            self,
            user_service: UserService,
            data: UserCreate = Body(media_type="application/json")
    ) -> UserResponse:
        
        try:
            user = await user_service.create(data)
            return UserResponse.model_validate(user)
        except ValueError as e:
            raise ValidationException(detail=str(e))

    @delete("/{user_id:str}")
    async def delete_user(
            self,
            user_service: UserService,
            user_id: str,
    ) -> None:
        
        success = await user_service.delete(user_id)
        if not success:
            raise NotFoundException(detail=f"User with ID {user_id} not found")

    @put("/{user_id:str}")
    async def update_user(
            self,
            user_service: UserService,
            user_id: str,
            data: UserUpdate = Body(media_type="application/json"),
    ) -> UserResponse:
        
        try:
            user = await user_service.update(user_id, data)
            if not user:
                raise NotFoundException(detail=f"User with ID {user_id} not found")
            return UserResponse.model_validate(user)
        except ValueError as e:
            raise ValidationException(detail=str(e))