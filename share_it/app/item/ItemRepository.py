from sqlalchemy import select, update, or_, and_


from share_it.app.core.db import AsyncSessionLocal
from share_it.app.item.ItemModel import Item
from share_it.app.item.ItemUserModel import Item_User


class ItemRepository:
    async def create_item(self, item: Item, session: AsyncSessionLocal):
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    async def create_item_user(self, item_user: Item_User, session: AsyncSessionLocal):
        session.add(item_user)
        await session.commit()

    async def update_item(self, session: AsyncSessionLocal, id: int, params: dict):
        item_update = await session.execute(update(Item).where(Item.id == id).values(**params))
        await session.commit()
        item = await session.execute(select(Item).where(Item.id == id))
        item_update = item.scalars().first()
        return item_update

    async def get_item_by_id(self, session: AsyncSessionLocal, id: int):
        db_item = await session.execute(
            select(Item).where(Item.id == id)
        )
        user = db_item.scalars().first()
        return user

    async def get_user_by_item(self, item_id: int, session: AsyncSessionLocal):
        db_item = await session.execute(
            select(Item_User.user_id).where(Item_User.item_id == item_id)
        )
        user = db_item.scalars().first()
        return user

    async def get_items_of_user(self, user_id: int, session: AsyncSessionLocal):
        db_items = await (session.execute(select(Item).
                          join(Item_User, Item.id == Item_User.item_id).
                          where(Item_User.user_id == user_id)))
        items = db_items.scalars().all()
        return items

    async def search_items(self, session: AsyncSessionLocal, text: str):
        search_lower = f'%{text.lower()}%'
        search_capital = f'%{text.capitalize()}%'
        db_items = await session.execute(select(Item).
                                         where(and_(or_(Item.name.like(search_lower),
                                                   Item.name.like(search_capital),
                                                   Item.description.like(search_lower),
                                                   Item.description.like(search_capital)),
                                                    Item.available == 1)))
        items = db_items.scalars().all()
        return items
