from uuid import UUID, uuid4
from typing import Optional, Union, List
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum, unique
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")



# class Gender(str, Enum):
#     male = "male"
#     female = "female"


# class Role(str, Enum):
#     admin = "admin"
#     user = "user"
#     student = "student"


# class Image(BaseModel):
#     url: HttpUrl
#     name: str


# class User(Base):
#     id: Union[UUID, None] = uuid4()
#     first_name: str = Field(max_length=100, description="first name of the user")
#     last_name: str = Field(max_length=100, description="last name of the user")
#     middle_name: Union[str, None] = Field(max_length=100, description="middle name of the user", default=None)
#     gender: Gender = Field(description="Gender of the user")
#     age: int = Field(gt=18, description="Age of the user")
#     roles: List[Role]
#     active: Union[bool, None] = False
#     image: Union[Image, None] = None