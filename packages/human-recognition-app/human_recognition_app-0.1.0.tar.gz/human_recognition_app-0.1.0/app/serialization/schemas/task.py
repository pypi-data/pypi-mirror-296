from uuid import UUID

from app.serialization.base_schema import Schema
from app.serialization.schemas import ImageSchema
from app.serialization.types import ShortFloat
from pydantic import Field


class TaskSchema(Schema):
    id: UUID = Field(examples=["e6088ffa-100e-4348-8967-8b0b6a3fff99"])
    images: list[ImageSchema]

    total_faces: int = Field(examples=[1])
    total_males: int = Field(examples=[1])
    total_females: int = Field(examples=[0])
    average_male_age: ShortFloat = Field(examples=[24.00])
    average_female_age: ShortFloat = Field(examples=[0.00])
