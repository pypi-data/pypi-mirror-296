from typing import Type, Container, Any

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .loader import SqlAlchemyPydanticLoader
from .mapper import SqlAlchemyPydanticMapper, default_mapper


class AlchemyPydanticMixim:
    mapper__: SqlAlchemyPydanticMapper = default_mapper

    async def to_pydantic(self, session: AsyncSession | None, depth: int = 5) -> BaseModel:
        loader = SqlAlchemyPydanticLoader(
            _mapper=self.mapper__,
            async_bind_factory=lambda: session
        )
        return await loader.load(self, depth=depth)

    def to_pydantic_sync(self, session: Session | None, depth: int = 5) -> BaseModel:
        loader = SqlAlchemyPydanticLoader(
            _mapper=self.mapper__,
            session=session
        )
        return loader.load_sync(self, depth)

    async def to_dict(self, session: AsyncSession | None, depth: int = 5) -> dict[str, Any]:
        loader = SqlAlchemyPydanticLoader(
            _mapper=self.mapper__,
            async_bind_factory=lambda: session
        )
        return await loader.load(self, depth=depth, mode="json")

    def to_dict_sync(self, session: Session | None, depth: int = 5):
        loader = SqlAlchemyPydanticLoader(
            _mapper=self.mapper__,
            session=session
        )
        return loader.load_sync(self, depth, mode="json")

    @classmethod
    def load(
            cls,
            model: Type = None,
            config: Type = None,
            exclude: Container[str] = None,
            model_name: str = None,
    ):
        return cls.mapper__.type(
            cls,
            config=config,
            exclude=exclude,
            model_name=model_name
        )(
            model or type(model_name or cls.__name__, (), {}))
