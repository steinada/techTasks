from typing import Optional
from pydantic import BaseModel, Field


class ItemDTO(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    available: bool


class ItemDB(ItemDTO):
    id: int

    class Config:
        from_attributes = True


class ItemUpdate(ItemDTO):
    name: str = Field(min_length=1, max_length=100, default=None)
    description: Optional[str] = None
    available: bool = None
