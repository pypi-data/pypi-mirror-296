from app.serialization.base_schema import Schema
from app.utils.gender_enum import GenderEnum
from pydantic import Field


class BoundingBox(Schema):
    height: int = Field(examples=["159"])
    width: int = Field(examples=["114"])
    x: int = Field(examples=["228"])
    y: int = Field(examples=["202"])


class FaceSchema(Schema):
    bbox: BoundingBox
    gender: GenderEnum = Field(examples=["male"])
    age: float = Field(examples=[24.00])
