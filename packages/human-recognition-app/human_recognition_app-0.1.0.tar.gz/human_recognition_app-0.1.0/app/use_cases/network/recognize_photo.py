import json
from typing import AsyncGenerator

from app.network.client import NetworkClient
from fastapi import status


class RecognizePhotoUseCase:
    async def execute(self, photo: AsyncGenerator[bytes, None]) -> dict | None:
        async with NetworkClient().client.post(
            "/api/v1/detect",
            params={
                "demographics": "true",
            },
            headers={
                "content-type": "image/jpeg",
            },
            data=photo,
        ) as response:
            binary_data = await response.read()
            data = json.loads(binary_data)
            if response.status == status.HTTP_200_OK:
                return data
            return None
