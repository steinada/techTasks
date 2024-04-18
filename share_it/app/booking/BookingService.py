from share_it.app.booking.BookingRepository import BookingRepository
from share_it.app.item.ItemRepository import ItemRepository
from share_it.app.user.UserRepository import UserRepository
from share_it.app.booking.BookingModel import Booking
from share_it.app.item.ItemModel import Item
from share_it.app.user.UserModel import User
from share_it.app.booking.BookingDB import BookingDB, BookingDTO, BookingStatus
from share_it.app.core.db import AsyncSessionLocal

from datetime import datetime

from fastapi import HTTPException

from http import HTTPStatus


class BookingService:
    def __init__(self):
        self.booking_repository = BookingRepository()
        self.item_repository = ItemRepository()
        self.user_repository = UserRepository()

    @staticmethod
    async def date_check(start, end):
        now = datetime.now()
        if start > end:
            raise HTTPException(HTTPStatus.BAD_REQUEST.value, "Start date is after end date")
        if end.date() < now.date():
            raise HTTPException(HTTPStatus.BAD_REQUEST.value, "End date is in past")
        if end == start:
            raise HTTPException(HTTPStatus.BAD_REQUEST.value, "Start is equal end")
        if start.date() < now.date():
            raise HTTPException(HTTPStatus.BAD_REQUEST.value, "Start date is in past")

    @staticmethod
    async def make_booking_model(bookings: list[dict]) -> list:
        booking_list = list()
        for booking in bookings:
            booking_model = BookingDB(**vars(booking['booking']))
            booking_model.booker = booking['user']
            booking_model.item = booking['item']
            booking_list.append(booking_model)
        return booking_list

    @staticmethod
    async def make_where_block(state: str | None, owner: bool) -> str:
        if owner:
            where = 'iu.user_id == user_id'
        else:
            where = 'b.booker_id == user_id'
        if state and state != 'ALL':
            date_now = datetime.now()
            if state == 'CURRENT':
                where = (f'and_({where},'
                         f'b.start < datetime({date_now.year}, {date_now.month}, {date_now.day}, {date_now.hour}, {date_now.minute}, {date_now.second}),'
                         f'b.end > datetime({date_now.year}, {date_now.month}, {date_now.day}, {date_now.hour}, {date_now.minute}, {date_now.second}))')
            elif state == 'FUTURE':
                where = f'and_({where}, b.start > datetime({date_now.year}, {date_now.month}, {date_now.day}, {date_now.hour}, {date_now.minute}, {date_now.second}))'
            elif state == 'PAST':
                where = f'and_({where}, b.end < datetime({date_now.year}, {date_now.month}, {date_now.day}, {date_now.hour}, {date_now.minute}, {date_now.second}))'
            else:
                try:
                    where = f'and_({where}, b.status == {BookingStatus[state]})'
                except:
                    raise HTTPException(HTTPStatus.BAD_REQUEST.value, f"Unknown state: {state}")
        return where

    async def book_item(self, booker_id: int,  booking_dto: BookingDTO, session: AsyncSessionLocal):
        params = booking_dto.dict()
        params['item_id'] = params['itemId']
        del params['itemId']

        item_is_present = await self.item_repository.get_item_and_owner_by_item_id(session=session,
                                                                                   item_id=params['item_id'])
        user_is_present = await self.user_repository.get_user_by_id(session=session, id=booker_id)
        if not item_is_present:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Item not found")
        if not user_is_present:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "User not found")
        await self.date_check(start=booking_dto.start, end=booking_dto.end)
        check_item_unavailable = await self.booking_repository.get_rent_dates(session=session, item_id=booking_dto.itemId,
                                                                  start=booking_dto.start, end=booking_dto.end)
        if not item_is_present['item'].available:
            raise HTTPException(HTTPStatus.BAD_REQUEST.value, "Item is unavailable")
        if check_item_unavailable:
            raise HTTPException(HTTPStatus.BAD_REQUEST.value, "Item is unavailable")
        if item_is_present['owner_id'] == booker_id:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Item is unavailable for booking by you")
        booking_model = Booking(**params, booker_id=booker_id)
        booking = await self.booking_repository.book_item(booking=booking_model, session=session)
        booking_info = await self.booking_repository.get_booking_info(session=session, booking_id=booking.id)
        user = booking_info.booker
        item = booking_info.item
        booking_model = await self.make_booking_model([{'user': user, 'item': item, 'booking': booking_info}])
        return booking_model[0]

    async def change_booking_status(self, user_id: int, booking_id: int, approved: bool, session: AsyncSessionLocal):
        booking_check_user = await self.booking_repository.check_user_booked_item(user_id=user_id, booking_id=booking_id,
                                                                    session=session)
        if not booking_check_user:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Incorrect user")
        current_booking_status = booking_check_user.status
        if approved:
            status = BookingStatus.APPROVED
            if current_booking_status.value == status.value:
                raise HTTPException(HTTPStatus.BAD_REQUEST.value, "Booking has been approved yet")
        else:
            status = BookingStatus.REJECTED
        booking_update = await self.booking_repository.change_booking_status(session=session, booking_id=booking_id,
                                                                             status=status)
        booking_info = await self.booking_repository.get_booking_info(session=session, booking_id=booking_id)
        user = booking_info.booker
        item = booking_info.item
        booking_model = await self.make_booking_model([{'user': user, 'item': item, 'booking': booking_info}])
        return booking_model[0]

    async def get_booking_by_id(self, booking_id: int, session: AsyncSessionLocal, user_id: int):
        booking_info = await self.booking_repository.get_booking_by_id(session=session, booking_id=booking_id)
        if not booking_info:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Booking not found")
        user = booking_info.booker
        item = booking_info.item
        if user_id != item.item_owner[0].id and booking_info.booker_id != user_id:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Incorrect user")
        booking_model = await self.make_booking_model([{'user': user, 'item': item, 'booking': booking_info}])
        return booking_model[0]

    async def get_bookings(self, user_id: int, state: str | None, session: AsyncSessionLocal, owner=False):
        where = await self.make_where_block(state=state, owner=owner)
        bookings = await self.booking_repository.get_bookings(where=where, user_id=user_id, session=session)
        if not bookings:
            raise HTTPException(HTTPStatus.NOT_FOUND.value, "Incorrect user")
        bookings_list = list()
        for booking_info in bookings:
            user = booking_info.booker
            item = booking_info.item
            bookings_list.append({'user': user, 'item': item, 'booking': booking_info})
        booking_models = await self.make_booking_model(bookings_list)
        return booking_models
