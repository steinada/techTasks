from sqlalchemy import select, update, or_, and_
from sqlalchemy.orm import aliased
import datetime


from share_it.app.core.db import AsyncSessionLocal
from share_it.app.item.ItemModel import Item
from share_it.app.item.ItemUserModel import Item_User
from share_it.app.item.CommentDTO import CommentDTO


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
        item = db_item.scalars().first()
        return item

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

    async def get_item_and_owner_by_item_id(self, session: AsyncSessionLocal, item_id: int):
        result = await session.execute(select(Item)
                                       .where(Item.id == item_id))
        result = result.scalars().first()
        if result:
            return {'item': result, 'owner_id': result.item_owner[0].user_id}
        else:
            return None

    async def get_item_with_bookings_by_id(self, session: AsyncSessionLocal, item_id: int):
        comments_db = await session.execute(select(Item)
                                            .where(Item.id == item_id))
        comments = comments_db.scalars().first()
        return comments

    async def get_items_with_bookings_by_id(self, session: AsyncSessionLocal, user_id: int):
        i, iu = aliased(Item), aliased(Item_User)
        result = await session.execute(select(i)
                                       .join(iu, iu.item_id == i.id, isouter=True)
                                       .where(iu.user_id == user_id))
        result = result.scalars().all()
        return result

    async def add_comment(self, session: AsyncSessionLocal, comment: CommentDTO):
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment
