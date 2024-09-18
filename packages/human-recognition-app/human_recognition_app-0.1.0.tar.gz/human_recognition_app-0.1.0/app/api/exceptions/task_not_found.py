from app.utils.http_docs_exception import HTTPDocsException
from fastapi import status


class TaskNotFoundException(HTTPDocsException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found",
        )
