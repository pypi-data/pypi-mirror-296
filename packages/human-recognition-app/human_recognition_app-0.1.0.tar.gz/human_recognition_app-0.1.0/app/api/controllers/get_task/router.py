from typing import Annotated
from uuid import UUID

from app.api.dependencies import SessionDep
from app.api.controllers.get_task.controller import GetTaskController
from app.api.controllers.get_task.responses import get_task_responses
from app.serialization.schemas import TaskSchema
from fastapi import APIRouter, Depends, status

get_task_router = APIRouter()


@get_task_router.get(
    path="/",
    response_model=TaskSchema,
    status_code=status.HTTP_200_OK,
    summary="Get a recognized task by id.",
    responses=get_task_responses,
)
async def get_task(
    controller: Annotated[GetTaskController, Depends(lambda: GetTaskController())],
    id: UUID,
    session: SessionDep,
) -> TaskSchema:
    return await controller.execute(id, session)
