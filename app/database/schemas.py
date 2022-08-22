from typing import Union

from pydantic import BaseModel
from pydantic import EmailStr

from fastapi import Form


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str
    city: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True