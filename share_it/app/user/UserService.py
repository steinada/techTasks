from fastapi import HTTPException

from http import HTTPStatus

from share_it.app.user.UserDTO import UserDTO
from share_it.app.user.UserModel import User
from share_it.app.user.UserRepository import UserRepository
from share_it.app.core.db import AsyncSessionLocal


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def user_create(self, user: UserDTO, session: AsyncSessionLocal):
        same_email = await self.user_repository.get_user_id_by_email(user.email, session)
        if same_email.all():
            raise HTTPException(HTTPStatus.CONFLICT.value, "Email is already used")
        user_params = user.dict()
        db_user = User(**user_params)
        new_user = await self.user_repository.create_user(db_user, session)
        return new_user

    async def user_update(self, session: AsyncSessionLocal, user: UserDTO, id: int):
        user_for_update = await self.user_repository.get_user_by_id(id=id, session=session)
        if user_for_update:
            new_params = user.model_dump(exclude_unset=True)
            try:
                updated_user = await self.user_repository.update_user(id=id, session=session, params=new_params)
                return updated_user
            except:
                raise HTTPException(HTTPStatus.CONFLICT.value, "Email is already used")
        else:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "User not found")

    async def get_all_users(self, session: AsyncSessionLocal):
        users = await self.user_repository.get_all_users(session)
        return users

    async def get_user_by_id(self, session: AsyncSessionLocal, id: int):
        user = await self.user_repository.get_user_by_id(session=session, id=id)
        if user is None:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "User not found")
        return user

    async def delete_user_by_id(self, session: AsyncSessionLocal, id: int):
        user = await self.user_repository.get_user_by_id(session=session, id=id)
        if not user:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "User not found")
        await self.user_repository.delete_user(session=session, user=user)
