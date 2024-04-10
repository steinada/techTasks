from sqlalchemy import select, update, or_, and_, desc, asc
from sqlalchemy.orm import aliased
import datetime


from share_it.app.core.db import AsyncSessionLocal
from share_it.app.item.ItemModel import Item
from share_it.app.item.ItemUserModel import Item_User
from share_it.app.item.CommentDTO import CommentDTO
from share_it.app.booking.BookingModel import Booking, BookingStatus


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

    async def get_item_name_by_id(self, session: AsyncSessionLocal, item_id: int):
        db_item = await session.execute(
            select(Item.name).where(Item.id == item_id)
        )
        item = db_item.scalars().first()
        return item

    async def change_item_available(self, session: AsyncSessionLocal, id: int, available: bool):
        item_update = await session.execute(update(Item).where(Item.id == id).values(available=available))
        await session.commit()
        item = await session.execute(select(Item).where(Item.id == id))
        item_update = item.scalars().first()
        return item_update

    async def get_item_and_owner_by_item_id(self, session: AsyncSessionLocal, item_id: int):
        i, iu = aliased(Item), aliased(Item_User)
        result = await session.execute(select(i, iu.user_id)
                                       .join(iu, i.id == iu.item_id, isouter=True)
                                       .where(i.id == item_id))
        result = result.first()
        if result:
            return {'item': result[0], 'owner_id': result[1]}
        else:
            return None

    async def get_item_with_bookings_by_id(self, session: AsyncSessionLocal, current_date: datetime.date,
                                           item_id: int):
        i, iu = aliased(Item), aliased(Item_User)
        bl = (select(Booking)
              .where(and_(Booking.item_id == item_id,
                          Booking.start < current_date,
                          Booking.status != BookingStatus.REJECTED.name))
              .order_by(desc(Booking.start))
              .limit(1).subquery())
        bn = (select(Booking)
              .where(and_(Booking.item_id == item_id,
                          Booking.start > current_date,
                          Booking.status != BookingStatus.REJECTED.name))
              .order_by(asc(Booking.start))
              .limit(1).subquery())
        result = await session.execute(select(i, bl.c.id, bl.c.booker_id, bn.c.id, bn.c.booker_id, iu.user_id)
                                       .join(bl, bl.c.item_id == i.id, isouter=True)
                                       .join(bn, bn.c.item_id == i.id, isouter=True)
                                       .join(iu, iu.item_id == i.id, isouter=True)
                                       .where(i.id == item_id))
        result = result.first()
        return result

    async def get_items_with_bookings_by_id(self, session: AsyncSessionLocal, current_date: datetime.date, user_id: int):
        i, iu = aliased(Item), aliased(Item_User)
        bl = (select(Booking)
              .where(and_(Booking.start < current_date,
                          Booking.status != BookingStatus.REJECTED.name))
              .order_by(desc(Booking.start))
              .limit(1).subquery())
        bn = (select(Booking)
              .where(and_(Booking.start > current_date,
                          Booking.status != BookingStatus.REJECTED.name))
              .order_by(asc(Booking.start))
              .limit(1).subquery())
        result = await session.execute(select(i, bl.c.id, bl.c.booker_id, bn.c.id, bn.c.booker_id, iu.user_id)
                                       .join(bl, bl.c.item_id == i.id, isouter=True)
                                       .join(bn, bn.c.item_id == i.id, isouter=True)
                                       .join(iu, iu.item_id == i.id, isouter=True)
                                       .where(iu.user_id == user_id))
        result = result.all()
        return result

    async def get_bookers_of_item(self, session: AsyncSessionLocal, item_id: int):
        i, b = aliased(Item), aliased(Booking)
        bookers = await session.execute(select(b.booker_id)
                                        .join(b, b.item_id == i.id, isouter=True)
                                        .where(i.id == item_id))
        bookers = bookers.scalars().first()
        return bookers

    async def add_comment(self, session: AsyncSessionLocal, comment: CommentDTO):
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment

