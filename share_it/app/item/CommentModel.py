from share_it.app.core.db import Base
from sqlalchemy import Column, Integer, Text, DateTime


class Comment(Base):
    item_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=True)
    text = Column(Text, nullable=False)
    created = Column(DateTime, nullable=False)
