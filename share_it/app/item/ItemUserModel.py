from sqlalchemy import Column, Integer, ForeignKey
from share_it.app.core.db import Base


class Item_User(Base):
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
