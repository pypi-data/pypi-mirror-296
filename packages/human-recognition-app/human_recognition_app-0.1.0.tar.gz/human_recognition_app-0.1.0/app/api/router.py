from app.api.controllers.add_task.router import add_task_router
from app.api.controllers.delete_task.router import delete_task_router
from app.api.controllers.get_task.router import get_task_router
from app.api.controllers.update_task.router import update_task_router
from app.api.dependencies import AuthDep
from app.api.exceptions import InvalidAuthDataException, NotAuthenticatedException
from fastapi import APIRouter, status, Depends

from app.use_cases.utils.security import SecurityUseCase

task_router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "problems with authentication",
            "content": {
                "application/json": {
                    "examples": {
                        **NotAuthenticatedException().example,
                        **InvalidAuthDataException().example,
                    },
                },
            },
        },
    },
    dependencies=[
        AuthDep,
    ]
)

task_router.include_router(add_task_router)
task_router.include_router(get_task_router)
task_router.include_router(delete_task_router)
task_router.include_router(update_task_router)
