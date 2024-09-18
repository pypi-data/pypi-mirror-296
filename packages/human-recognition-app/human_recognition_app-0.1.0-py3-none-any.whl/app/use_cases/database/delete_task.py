from uuid import UUID

from app.database.models import ImageModel, TaskModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class DeleteTaskUseCase:
    async def execute(
        self,
        id: UUID,
        session: AsyncSession,
    ) -> list[UUID] | None:
        task_ids_query = select(ImageModel.id).filter_by(task_id=id)
        task_ids_result = await session.execute(task_ids_query)
        task_ids = task_ids_result.scalars().all()

        if not task_ids:
            return None

        query = delete(TaskModel).filter_by(id=id)
        await session.execute(query)
        await session.flush()
        return task_ids
