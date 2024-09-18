from typing import Annotated
from uuid import UUID

from app.api.dependencies import SessionDep
from app.api.controllers.update_task.controller import UpdateTaskController
from app.api.controllers.update_task.responses import update_task_responses
from fastapi import APIRouter, Depends, UploadFile, status

update_task_router = APIRouter()


@update_task_router.patch(
    path="/",
    response_model=UUID,
    status_code=status.HTTP_200_OK,
    summary="update recognized task by id.",
    responses=update_task_responses,
)
async def update_task(
    controller: Annotated[UpdateTaskController, Depends(lambda: UpdateTaskController())],
    id: UUID,
    photo: UploadFile,
    session: SessionDep,
) -> UUID:
    return await controller.execute(id, photo, session)
