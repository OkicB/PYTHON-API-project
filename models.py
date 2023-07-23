from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from main import Base
from enum import Enum
from sqlalchemy import Column, String, Enum as DBEnum
from sqlalchemy.dialects.postgresql import UUID

class Gender(str, Enum):
    male = 'male'
    female = 'female'

class Role(str, Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = 'users'
    id: Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name: Column(String, nullable=False)
    last_name: Column(String, nullable=False)
    gender: Column(DBEnum(Gender), nullable=False)
    roles: Column(DBEnum(Role, create_constraint=False), nullable=False)

class UpdateUser(Base):
    first_name: Column(String, nullable=False)
    last_name: Column(String, nullable=False)
    roles: Column(DBEnum(Role, create_constraint=False), nullable=False)