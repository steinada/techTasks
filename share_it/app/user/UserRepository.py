from sqlalchemy import select, update

from share_it.app.core.db import AsyncSessionLocal
from share_it.app.user.UserModel import User


class UserRepository:
    async def create_user(self, db_user: User, session: AsyncSessionLocal):
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    async def get_user_id_by_email(self, user_email: str, session: AsyncSessionLocal):
        result = await session.execute(
            select(User.id).where(User.email == user_email)
        )
        return result

    async def update_user(self, id: int, session: AsyncSessionLocal, params: dict):
        user_update = await session.execute(update(User).where(User.id == id).values(**params))
        await session.commit()
        user = await session.execute(select(User).where(User.id == id))
        user_update = user.scalars().first()
        return user_update

    async def get_all_users(self, session: AsyncSessionLocal):
        db_users = await session.execute(select(User))
        db_users = db_users.scalars().all()
        return db_users

    async def get_user_by_id(self, id: int, session: AsyncSessionLocal):
        db_user = await session.execute(
            select(User).where(User.id == id)
        )
        user = db_user.scalars().first()
        return user

    async def delete_user(self, user: User, session: AsyncSessionLocal):
        await session.delete(user)
        await session.commit()

    async def get_user_name(self, session: AsyncSessionLocal, user_id: int):
        user_name = await session.execute(select(User.name)
                                        .where(User.id == user_id))
        user_name = user_name.scalars().first()
        return user_name

