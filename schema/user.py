from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from model.user import UserBase
from schema.role import IRoleRead


class IUserRegister(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    password: str
    phone: Optional[str]
    birthdate: Optional[datetime]


class IUserCreate(IUserRegister, smart_union=True, orm_mode=True):
    is_superuser: bool = False
    role_id: int = 1


class IUserRead(UserBase):
    id: int
    role: Optional[IRoleRead] = None


class IUserUpdate(BaseModel):
    id: int
    email: EmailStr
    is_active: bool = True
