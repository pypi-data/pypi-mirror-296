import asyncio
import os
from uuid import UUID

from app.api.exceptions import TaskNotFoundException
from app.use_cases.database import DeleteTaskUseCase
from app.use_cases.file_system import DeleteFileUseCase
from sqlalchemy.ext.asyncio import AsyncSession


class DeleteTaskController:
    _delete_task = DeleteTaskUseCase().execute
    _delete_file = DeleteFileUseCase().execute

    async def execute(
        self,
        id: UUID,
        session: AsyncSession,
    ) -> UUID:
        async with session:
            image_ids = await self._delete_task(id, session)
            if not image_ids:
                raise TaskNotFoundException()

            paths = [
                os.path.join(os.getcwd(), "temp", str(image_id))
                for image_id in image_ids
            ]
            await asyncio.gather(*[self._delete_file(path) for path in paths])
            await session.commit()
            return id
