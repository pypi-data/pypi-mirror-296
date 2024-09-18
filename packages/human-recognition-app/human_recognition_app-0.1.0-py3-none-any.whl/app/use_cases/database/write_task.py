from uuid import UUID

from app.database.models import FaceModel, ImageModel, TaskModel
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


class WriteTaskUseCase:
    async def execute(
        self,
        photos: list[UploadFile],
        recognition_results: list[dict],
        uuids: list[UUID],
        session: AsyncSession,
    ) -> UUID:
        task = TaskModel(
            images=[],
        )
        for photo, uuid, res in zip(photos, uuids, recognition_results):
            image = ImageModel(
                id=uuid,
                name=photo.filename,
                faces=[],
            )
            task.images.append(image)
            for face in res["data"]:
                face_model = FaceModel(
                    bbox_height=face["bbox"]["height"],
                    bbox_width=face["bbox"]["width"],
                    bbox_x=face["bbox"]["x"],
                    bbox_y=face["bbox"]["y"],
                    gender=face["demographics"]["gender"].upper(),
                    age=face["demographics"]["age"]["mean"],
                )
                image.faces.append(face_model)
        session.add(task)
        await session.flush()
        return task.id
