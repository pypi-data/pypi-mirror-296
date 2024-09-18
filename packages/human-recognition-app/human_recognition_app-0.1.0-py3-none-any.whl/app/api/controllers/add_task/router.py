from typing import Annotated
from uuid import UUID

from app.api.dependencies import SessionDep
from app.api.controllers.add_task.controller import AddTaskController
from app.api.controllers.add_task.responses import add_task_responses
from fastapi import APIRouter, Depends, UploadFile, status

add_task_router = APIRouter()


@add_task_router.post(
    path="/",
    response_model=UUID,
    status_code=status.HTTP_201_CREATED,
    summary="Add a task with photos to recognize people on them.",
    responses=add_task_responses,
)
async def add_task(
    controller: Annotated[AddTaskController, Depends(lambda: AddTaskController())],
    photos: list[UploadFile],
    session: SessionDep,
) -> UUID:
    return await controller.execute(photos, session)
