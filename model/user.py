from sqlmodel import Field, SQLModel, Relationship, Column, DateTime
from pydantic import EmailStr
from typing import Optional
from datetime import datetime


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(nullable=True, index=True, sa_column_kwargs={'unique': True})
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    birthdate: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True))
    phone: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    hashed_password: str = Field(
        nullable=False, index=True
    )
    role_id: Optional[int] = Field(default=None, foreign_key='role.id')
    role: Optional['Role'] = Relationship(back_populates='users')

