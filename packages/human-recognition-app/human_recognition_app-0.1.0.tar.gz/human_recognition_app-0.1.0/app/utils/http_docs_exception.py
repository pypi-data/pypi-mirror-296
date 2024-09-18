from abc import ABC

from fastapi import HTTPException


class HTTPDocsException(HTTPException, ABC):
    def __init__(
        self,
        status_code: int,
        detail: str,
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )

    @property
    def example(self) -> dict:
        return {
            self.detail: {
                "value": {
                    "detail": self.detail,
                },
            },
        }
