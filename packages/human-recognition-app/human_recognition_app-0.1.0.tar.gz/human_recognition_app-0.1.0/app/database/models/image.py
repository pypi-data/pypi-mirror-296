from app.database.base_model import Model
from app.database.types import PKModelType
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ImageModel(Model):
    __tablename__ = "image"

    id: PKModelType
    task_id: Mapped[str] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))
    name: Mapped[str]

    faces: Mapped[list["FaceModel"]] = relationship(
        back_populates="image", cascade="all,delete",
    )

    task: Mapped["TaskModel"] = relationship(
        "TaskModel",
        back_populates="images",
    )
