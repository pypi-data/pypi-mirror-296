from app.database.base_model import Model
from app.database.types import GenderModelType, PKModelType
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class FaceModel(Model):
    __tablename__ = "face"

    id: PKModelType
    image_id: Mapped[str] = mapped_column(ForeignKey("image.id", ondelete="CASCADE"))
    bbox_height: Mapped[int]
    bbox_width: Mapped[int]
    bbox_x: Mapped[int]
    bbox_y: Mapped[int]
    gender: GenderModelType
    age: Mapped[int]

    image: Mapped["ImageModel"] = relationship(
        "ImageModel",
    )
