from app.utils.http_docs_exception import HTTPDocsException
from fastapi import status


class WrongMimetypeException(HTTPDocsException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'image/jpeg' request mimetype is required",
        )
