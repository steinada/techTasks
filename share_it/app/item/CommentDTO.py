from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CommentDTO(BaseModel):
    item_id: Optional[int] = None
    user_id: Optional[int] = None
    text: Optional[str] = Field(min_length=1, max_length=1000, default=None)
    created: Optional[datetime] = None


class CommentDB(CommentDTO):
    id: int
    authorName: Optional[str]

    class Config:
        from_attributes = True


