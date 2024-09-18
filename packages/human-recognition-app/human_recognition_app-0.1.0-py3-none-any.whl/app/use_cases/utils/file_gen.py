from typing import AsyncGenerator

from fastapi import UploadFile


class FileGenUseCase:
    async def _file_gen(
        self,
        file: UploadFile,
        chunk_size: int = 1024,
    ) -> AsyncGenerator[bytes, None]:
        chunk = await file.read(chunk_size)
        while chunk:
            yield chunk
            chunk = await file.read(chunk_size)

    def execute(
        self,
        file: UploadFile,
        chunk_size: int = 1024,
    ) -> AsyncGenerator[bytes, None]:
        return self._file_gen(
            file,
            chunk_size,
        )
