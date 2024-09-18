from app.api.exceptions import TaskNotFoundException
from starlette import status

get_task_responses = {
    status.HTTP_200_OK: {
        "description": "Successfully returned task.",
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
