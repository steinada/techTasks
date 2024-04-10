from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from share_it.app.booking.BookingStatus import BookingStatus
from share_it.app.core.db import Base


class Booking(Base):
    start = Column(DateTime(), nullable=False)
    end = Column(DateTime(), nullable=False)
    status = Column(Enum(BookingStatus), nullable=False)
    booker_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
