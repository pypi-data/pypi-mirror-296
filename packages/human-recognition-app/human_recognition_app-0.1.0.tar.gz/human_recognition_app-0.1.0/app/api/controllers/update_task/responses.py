from app.api.exceptions import (
    FailedToDecodeImageException,
    TaskNotFoundException,
    WrongMimetypeException,
)
from starlette import status

update_task_responses = {
    status.HTTP_200_OK: {
        "description": "Task successfully updated.",
    },
    status.HTTP_400_BAD_REQUEST: {
        "description": "problems with image recognition",
        "content": {
            "application/json": {
                "examples": {
                    **WrongMimetypeException().example,
                    **FailedToDecodeImageException().example,
                },
            },
        },
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
