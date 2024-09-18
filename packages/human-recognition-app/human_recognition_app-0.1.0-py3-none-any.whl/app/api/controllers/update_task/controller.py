import os
from uuid import UUID, uuid4

from app.api.exceptions import (
    FailedToDecodeImageException,
    TaskNotFoundException,
    WrongMimetypeException,
)
from app.use_cases.database import TaskExistUseCase, WriteImageUseCase
from app.use_cases.file_system import DeleteFileUseCase, WriteFileUseCase
from app.use_cases.network import RecognizePhotoUseCase
from app.use_cases.utils import FileGenUseCase
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


class UpdateTaskController:
    _recognize_photo = RecognizePhotoUseCase().execute
    _write_file = WriteFileUseCase().execute
    _file_gen = FileGenUseCase().execute
    _write_image = WriteImageUseCase().execute
    _delete_file = DeleteFileUseCase().execute
    _task_exists = TaskExistUseCase().execute

    async def _process_photo(
        self,
        photo: UploadFile,
        path: str,
    ) -> dict | None:
        file_gen = self._file_gen(
            photo,
            1024,
        )
        file_gen_wrapper = self._write_file(file_gen, path)
        recognition_result = await self._recognize_photo(
            file_gen_wrapper,
        )
        return recognition_result

    async def execute(
        self,
        task_id: UUID,
        photo: UploadFile,
        session: AsyncSession,
    ) -> UUID:
        async with session:
            if photo.content_type != "image/jpeg":
                raise WrongMimetypeException()

            if not await self._task_exists(task_id, session):
                raise TaskNotFoundException()

            id = uuid4()
            path = os.path.join(os.getcwd(), "temp", str(id))
            try:
                recognition_result = await self._process_photo(photo, path)
                if not recognition_result:
                    raise FailedToDecodeImageException()
                await self._write_image(photo, recognition_result, id, task_id, session)
                await session.commit()
                return task_id
            except FailedToDecodeImageException as exception:
                await self._delete_file(path)
                raise exception
