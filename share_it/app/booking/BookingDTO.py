from pydantic import BaseModel

from datetime import datetime

from typing import Optional

from share_it.app.booking.BookingStatus import BookingStatus


class BookingDTO(BaseModel):
    start: datetime
    end: datetime
    status: BookingStatus = BookingStatus.WAITING.name
    itemId: int


class BookingUpdate(BookingDTO):
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    status: Optional[int] = None
    itemId: Optional[int] = None
