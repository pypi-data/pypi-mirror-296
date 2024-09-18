from aiohttp import ClientSession
from app.config.network import network_config
from singleton import Singleton


class NetworkClient(metaclass=Singleton):
    def __init__(self) -> None:
        self.client = ClientSession(
            base_url=network_config.base_url,
            headers={
                "Authorization": network_config.access_token,
            },
        )

    async def disconnect(self) -> None:
        await self.client.close()
