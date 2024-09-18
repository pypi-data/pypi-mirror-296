from app.api.exceptions import TaskNotFoundException
from starlette import status

delete_task_responses = {
    status.HTTP_200_OK: {
        "description": "Task successfully deleted.",
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "task not found",
        "content": {
            "application/json": {
                "examples": {
                    **TaskNotFoundException().example,
                },
            },
        },
    },
}
