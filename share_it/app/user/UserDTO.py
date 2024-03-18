from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserDTO(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class UserDB(UserDTO):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(UserDTO):
    name: Optional[str] = Field(max_length=100, default=None)
    email: EmailStr = None

