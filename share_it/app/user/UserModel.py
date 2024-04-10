from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from share_it.app.core.db import Base


class User(Base):
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    booker = relationship("Booking", backref="booker", lazy="selectin")
