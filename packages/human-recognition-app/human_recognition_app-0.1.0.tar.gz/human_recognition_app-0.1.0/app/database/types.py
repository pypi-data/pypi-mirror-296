from typing import Annotated
from uuid import uuid4

from app.utils.gender_enum import GenderEnum
from sqlalchemy import UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column

PKModelType = Mapped[
    Annotated[
        UUID,
        mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4),
    ]
]

GenderModelType = Mapped[
    Annotated[
        GenderEnum,
        mapped_column(Enum(GenderEnum)),
    ]
]
