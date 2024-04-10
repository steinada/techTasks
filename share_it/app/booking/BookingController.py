from fastapi import APIRouter, Depends, Header

from typing import Annotated

from share_it.app.booking.BookingDB import BookingDTO, BookingDB
from share_it.app.booking.BookingService import BookingService
from share_it.app.core.db import AsyncSessionLocal, get_async_session

router = APIRouter(prefix="/bookings", tags=["Bookings"])
booking_service = BookingService()


@router.post("", response_model=BookingDB, response_model_exclude_none=True)
async def book_item(x_sharer_user_id: Annotated[int | None, Header()],
                    booking_info: BookingDTO, session: AsyncSessionLocal = Depends(get_async_session)):
    booking_info = await booking_service.book_item(booker_id=x_sharer_user_id, booking_dto=booking_info, session=session)
    return booking_info


@router.patch("/{bookingId}", response_model=BookingDB, response_model_exclude_none=True)
async def change_booking_status(x_sharer_user_id: Annotated[int | None, Header()], bookingId: int, approved: bool,
                    session: AsyncSessionLocal = Depends(get_async_session)):
    booking_updated = await (booking_service.change_booking_status(session=session, user_id=x_sharer_user_id,
                                                                   booking_id=bookingId, approved=approved))
    return booking_updated


@router.get("", response_model=list[BookingDB], response_model_exclude_none=True)
async def get_booking(x_sharer_user_id: Annotated[int | None, Header()],
                      session: AsyncSessionLocal = Depends(get_async_session), state=None):
    bookings = await booking_service.get_bookings(session=session, user_id=x_sharer_user_id, state=state)
    return bookings


@router.get("/owner", response_model=list[BookingDB], response_model_exclude_none=True)
async def get_booking(x_sharer_user_id: Annotated[int | None, Header()],
                      session: AsyncSessionLocal = Depends(get_async_session), state=None):
    bookings = await booking_service.get_bookings(owner=True, session=session, user_id=x_sharer_user_id, state=state)
    return bookings


@router.get("/{bookingId}", response_model=BookingDB, response_model_exclude_none=True)
async def get_booking(x_sharer_user_id: Annotated[int | None, Header()], bookingId: int,
                    session: AsyncSessionLocal = Depends(get_async_session)):

    booking = await booking_service.get_booking_by_id(booking_id=bookingId, session=session, user_id=x_sharer_user_id)
    return booking
