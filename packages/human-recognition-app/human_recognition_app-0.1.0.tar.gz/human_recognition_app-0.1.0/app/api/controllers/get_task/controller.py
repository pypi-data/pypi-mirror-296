from uuid import UUID

from app.serialization.schemas import TaskSchema
from app.use_cases.database import ReadTaskUseCase
from sqlalchemy.ext.asyncio import AsyncSession


class GetTaskController:
    _read_task = ReadTaskUseCase().execute

    async def execute(
        self,
        uuid: UUID,
        session: AsyncSession,
    ) -> TaskSchema:
        async with session:
            task = await self._read_task(
                uuid,
                session,
            )
            await session.commit()
            return task
