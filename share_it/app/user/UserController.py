from fastapi import APIRouter, Depends

from share_it.app.user.UserDTO import UserDTO, UserDB, UserUpdate
from share_it.app.user.UserService import UserService
from share_it.app.core.db import AsyncSessionLocal, get_async_session


router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService()


@router.post("", response_model=UserDB, response_model_exclude_none=True)
async def create_user(user: UserDTO, session: AsyncSessionLocal = Depends(get_async_session)):
    new_user = await user_service.user_create(user, session)
    return new_user


@router.patch("/{userId}", response_model=UserDB, response_model_exclude_none=True)
async def update_user(user: UserUpdate, userId: int, session: AsyncSessionLocal = Depends(get_async_session)):
    updated_user = await user_service.user_update(user=user, id=userId, session=session)
    return updated_user


@router.get("", response_model=list[UserDB], response_model_exclude_none=True)
async def get_all_users(session: AsyncSessionLocal = Depends(get_async_session)):
    users = await user_service.get_all_users(session)
    return users


@router.get("/{userId}", response_model=UserDB, response_model_exclude_none=True)
async def get_user_by_id(userId, session: AsyncSessionLocal = Depends(get_async_session)):
    user = await user_service.get_user_by_id(id=userId, session=session)
    return user


@router.delete("/{userId}", response_model=dict)
async def delete_user_by_id(userId, session: AsyncSessionLocal = Depends(get_async_session)):
    await user_service.delete_user_by_id(id=userId, session=session)
    return {"result": "User deleted"}

