from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from share_it.app.core.db import Base


class Item(Base):
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=True)
    available = Column(Boolean, nullable=False)
    bookings = relationship("Booking", backref="booking", lazy="selectin")
    item_comments = relationship("Comment", backref="comments", lazy="selectin")
    item_owner = relationship("Item_User", backref="item_owner", lazy="selectin")
