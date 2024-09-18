from app.api.exceptions import FailedToDecodeImageException, WrongMimetypeException
from starlette import status

add_task_responses = {
    status.HTTP_201_CREATED: {
        "description": "Task was completed successfully.",
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
}
