from datetime import datetime
from typing import TypeVar, Generic, Type, Optional, Tuple, Union, T
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.async_sqlmodel import paginate
from sqlmodel.sql.expression import Select, SelectOfScalar

from pydantic import BaseModel
from sqlalchemy import select
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(
            self, id: int, db_session: AsyncSession
    ) -> Tuple[Optional[ModelType]]:
        response = await db_session.exec(select(self.model).where(self.model.id == id))
        return response.first()

    async def create(
            self, obj_in: CreateSchemaType, db_session: AsyncSession
    ) -> ModelType:
        db_obj = self.model.from_orm(obj_in)  # type: ignore
        db_obj.created_at = datetime.utcnow()
        db_obj.updated_at = datetime.utcnow()
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def delete(self, id: int, db_session: AsyncSession):
        response = await db_session.exec(select(self.model).where(self.model.id == id))
        obj = response.one()[0]
        await db_session.delete(obj)
        await db_session.commit()
        return obj

    async def get_multi_paginated(
        self, db_session: AsyncSession, params: Optional[Params] = Params(),
            query: Optional[Union[T, Select[T], SelectOfScalar[T]]] = None
    ) -> Page[ModelType]:
        if query is None:
            query = self.model
        return await paginate(db_session, query, params)

