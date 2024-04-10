from share_it.app.booking.BookingDTO import BookingDTO
from share_it.app.item.ItemDTO import ItemDB
from share_it.app.user.UserDTO import UserDB
from share_it.app.booking.BookingStatus import BookingStatus

from pydantic import field_serializer

from functools import singledispatchmethod

from typing import Optional


class BookingDB(BookingDTO):
    id: int
    booker: Optional[UserDB] = None
    item: Optional[ItemDB] = None
    itemId: Optional[int] = None

    @field_serializer('status')
    def _(self, value: BookingStatus):
        return value.name

    class Config:
        from_attributes = True


