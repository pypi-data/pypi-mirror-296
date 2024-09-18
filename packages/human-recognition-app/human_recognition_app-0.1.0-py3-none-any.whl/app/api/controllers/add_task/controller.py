import asyncio
import os.path
from uuid import UUID, uuid4

from app.api.exceptions import FailedToDecodeImageException
from app.api.exceptions.wrong_mime_type import WrongMimetypeException
from app.use_cases.database import WriteTaskUseCase
from app.use_cases.file_system import DeleteFileUseCase, WriteFileUseCase
from app.use_cases.network import RecognizePhotoUseCase
from app.use_cases.utils import FileGenUseCase
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


class AddTaskController:
    _recognize_photo = RecognizePhotoUseCase().execute
    _write_file = WriteFileUseCase().execute
    _delete_file = DeleteFileUseCase().execute
    _write_task = WriteTaskUseCase().execute
    _file_gen = FileGenUseCase().execute

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
        photos: list[UploadFile],
        session: AsyncSession,
    ) -> UUID:
        if any(photo.content_type != "image/jpeg" for photo in photos):
            raise WrongMimetypeException()

        uuids = [uuid4() for _ in photos]
        paths = [os.path.join(os.getcwd(), "temp", str(uuid)) for uuid in uuids]

        try:
            recognition_results = await asyncio.gather(
                *[
                    self._process_photo(photo, uuid)
                    for photo, uuid in zip(photos, paths)
                ],
            )
            if None in recognition_results:
                raise FailedToDecodeImageException()

            async with session:
                task_id = await self._write_task(
                    photos,
                    recognition_results,
                    uuids,
                    session,
                )
                await session.commit()
                return task_id
        except FailedToDecodeImageException as exception:
            await asyncio.gather(*[self._delete_file(path) for path in paths])
            raise exception
