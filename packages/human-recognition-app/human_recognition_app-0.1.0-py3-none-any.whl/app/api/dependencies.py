from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import InvalidAuthDataException
from app.database.client import DatabaseClient
from app.use_cases.utils.security import SecurityUseCase

SessionDep = Annotated[
    AsyncSession,
    Depends(DatabaseClient().get_session),
]


async def security(
    credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]
) -> None:
    if not await SecurityUseCase().execute(credentials):
        raise InvalidAuthDataException()


AuthDep = Depends(security)
