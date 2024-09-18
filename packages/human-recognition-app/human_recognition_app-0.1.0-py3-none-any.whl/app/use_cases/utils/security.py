from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from app.config.auth import auth_config


class SecurityUseCase:
    async def execute(
        self,
        credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]
    ) -> bool:
        return all((
            auth_config.username == credentials.username,
            auth_config.password == credentials.password,
        ))
