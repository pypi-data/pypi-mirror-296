import os

from fastapi.concurrency import run_in_threadpool


class DeleteFileUseCase:
    def _remove_file(
        self,
        path: str,
    ) -> None:
        os.remove(path)

    async def execute(
        self,
        path: str,
    ) -> None:
        await run_in_threadpool(self._remove_file, path)
