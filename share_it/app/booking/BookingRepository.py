from sqlalchemy import select, and_, update, desc, or_
from sqlalchemy.orm import aliased

import datetime

from share_it.app.booking.BookingModel import Booking
from share_it.app.booking.BookingStatus import BookingStatus
from share_it.app.item.ItemModel import Item
from share_it.app.item.ItemUserModel import Item_User
from share_it.app.user.UserModel import User
from share_it.app.core.db import AsyncSessionLocal


class BookingRepository:
    async def book_item(self, booking: Booking, session: AsyncSessionLocal):
        session.add(booking)
        await session.commit()
        await session.refresh(booking)
        return booking

    async def get_booking_info(self, booking_id: int, session: AsyncSessionLocal):
        u, i, b = aliased(User), aliased(Item), aliased(Booking)
        result = await session.execute(select(u, i, b)
                                     .join(i, b.item_id == i.id, isouter=True)
                                     .join(u, b.booker_id == u.id, isouter=True)
                                     .where(b.id == booking_id))
        result = result.first()
        return result

    async def check_user_booked_item(self, user_id: int, booking_id: Booking, session: AsyncSessionLocal):
        ui, b = aliased(Item_User), aliased(Booking)
        result = await session.execute(select(ui.item_id, b.id, b.status)
                                       .join(ui, ui.item_id == b.item_id, isouter=True)
                                       .where(and_(b.id == booking_id, ui.user_id == user_id)))
        result = result.first()
        return result

    async def change_booking_status(self, session: AsyncSessionLocal, booking_id: int, status: BookingStatus):
        booking_update = await session.execute(update(Booking).where(Booking.id == booking_id).values(status=status))
        await session.commit()
        booking = await session.execute(select(Booking).where(Booking.id == booking_id))
        booking_update = booking.scalars().first()
        return booking_update

    async def get_booking_by_id(self, session: AsyncSessionLocal, booking_id: int):
        u, i, b, iu = aliased(User), aliased(Item), aliased(Booking), aliased(Item_User)
        result = await session.execute(select(u, i, b, iu.user_id)
                                     .join(i, b.item_id == i.id, isouter=True)
                                     .join(u, b.booker_id == u.id, isouter=True)
                                     .join(iu, b.item_id == iu.item_id, isouter=True)
                                     .where(b.id == booking_id))
        result = result.first()
        return result

    async def get_bookings(self, session: AsyncSessionLocal, user_id: int, where: str):
        u, i, b, iu = aliased(User), aliased(Item), aliased(Booking), aliased(Item_User)
        result = await session.execute(select(u, i, b)
                                       .join(i, b.item_id == i.id, isouter=True)
                                       .join(u, b.booker_id == u.id, isouter=True)
                                       .join(iu, b.item_id == iu.item_id, isouter=True)
                                       .where(eval(where))
                                       .order_by(desc(b.start)))
        result = result.all()
        return result

    async def get_rent_dates(self, session: AsyncSessionLocal, item_id: int, start: datetime, end: datetime):
        result = await session.execute(select(Booking.start, Booking.end)
                                       .where(and_(Booking.item_id == item_id,
                                                   Booking.status != BookingStatus.REJECTED.name,
                                                   or_(and_(start <= Booking.start, Booking.start < end),
                                                   and_(start < Booking.end, Booking.end <= end))))
                                       .order_by(desc(Booking.start)))
        result = result.all()
        return result
