from app.serialization.base_schema import Schema
from app.serialization.schemas import FaceSchema
from pydantic import Field


class ImageSchema(Schema):
    name: str = Field(examples=["peoples.jpeg"])
    faces: list[FaceSchema]
