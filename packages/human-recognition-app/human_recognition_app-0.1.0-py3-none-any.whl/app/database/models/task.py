from app.database.base_model import Model
from app.database.types import PKModelType
from sqlalchemy.orm import Mapped, relationship


class TaskModel(Model):
    __tablename__ = "task"

    id: PKModelType

    images: Mapped[list["ImageModel"]] = relationship(
        back_populates="task", cascade="all,delete",
    )
