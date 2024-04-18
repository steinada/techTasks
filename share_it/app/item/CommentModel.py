from share_it.app.core.db import Base
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime


class Comment(Base):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    text = Column(Text, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.now())
    author = relationship("User", backref="author", lazy="selectin")
    # item = relationship("Item", backref="item", lazy="selectin")
