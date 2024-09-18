from uuid import UUID

from app.database.models import TaskModel
from sqlalchemy.ext.asyncio import AsyncSession


class TaskExistUseCase:
    async def execute(
        self,
        id: UUID,
        session: AsyncSession,
    ) -> bool:
        return bool(await session.get(TaskModel, id))
