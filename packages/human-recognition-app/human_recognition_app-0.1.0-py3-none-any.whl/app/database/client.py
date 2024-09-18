from app.config.database import database_config
from singleton import Singleton
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DatabaseClient(metaclass=Singleton):
    _engine: AsyncEngine | None = None
    _session_maker: async_sessionmaker[AsyncSession] | None = None

    async def get_session(self) -> AsyncSession:
        return self._session_maker()

    async def connect(self) -> None:
        if self._session_maker is None:
            self._engine = create_async_engine(
                database_config.url,
                pool_size=3,
                max_overflow=47,
            )
            self._session_maker = async_sessionmaker(
                self._engine,
            )

    async def disconnect(self) -> None:
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._session_maker = None
