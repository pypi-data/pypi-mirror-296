from typing import Annotated
from uuid import UUID

from app.api.dependencies import SessionDep
from app.api.controllers.delete_task.controller import DeleteTaskController
from app.api.controllers.delete_task.responses import delete_task_responses
from fastapi import APIRouter, Depends, status

delete_task_router = APIRouter()


@delete_task_router.delete(
    path="/",
    response_model=UUID,
    status_code=status.HTTP_200_OK,
    summary="Delete recognized task by id.",
    responses=delete_task_responses,
)
async def delete_task(
    controller: Annotated[DeleteTaskController, Depends(lambda: DeleteTaskController())],
    id: UUID,
    session: SessionDep,
) -> UUID:
    return await controller.execute(id, session)
