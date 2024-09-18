from typing import AsyncGenerator

import aiofile


class WriteFileUseCase:
    async def _write_file(
        self,
        file: AsyncGenerator[bytes, None],
        path: str,
    ) -> AsyncGenerator[bytes, None]:
        async with aiofile.async_open(path, "wb") as afp:
            async for chunk in file:
                await afp.write(chunk)
                yield chunk

    def execute(
        self,
        file: AsyncGenerator[bytes, None],
        path: str,
    ) -> AsyncGenerator[bytes, None]:
        return self._write_file(
            file,
            path,
        )
