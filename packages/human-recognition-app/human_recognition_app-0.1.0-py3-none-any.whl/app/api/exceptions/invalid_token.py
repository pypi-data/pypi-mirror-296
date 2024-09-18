from app.utils.http_docs_exception import HTTPDocsException
from fastapi import status


class InvalidAuthDataException(HTTPDocsException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid auth data",
        )
