from uuid import UUID

from app.database.models import FaceModel, ImageModel
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


class WriteImageUseCase:
    async def execute(
        self,
        photo: UploadFile,
        recognition_results: dict,
        id: UUID,
        task_id: UUID,
        session: AsyncSession,
    ) -> UUID:
        image = ImageModel(
            id=id,
            task_id=task_id,
            name=photo.filename,
            faces=[],
        )
        for face in recognition_results["data"]:
            face_model = FaceModel(
                bbox_height=face["bbox"]["height"],
                bbox_width=face["bbox"]["width"],
                bbox_x=face["bbox"]["x"],
                bbox_y=face["bbox"]["y"],
                gender=face["demographics"]["gender"].upper(),
                age=face["demographics"]["age"]["mean"],
            )
            image.faces.append(face_model)
        session.add(image)
        await session.flush()
        return task_id
