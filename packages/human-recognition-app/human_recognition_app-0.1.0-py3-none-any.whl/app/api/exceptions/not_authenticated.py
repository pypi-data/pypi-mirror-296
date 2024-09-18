from fastapi import status

from app.utils.http_docs_exception import HTTPDocsException


class NotAuthenticatedException(HTTPDocsException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
