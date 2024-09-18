from statistics import mean
from uuid import UUID

from app.database.models import FaceModel, ImageModel, TaskModel
from app.serialization.schemas import BoundingBox, FaceSchema, ImageSchema, TaskSchema
from app.utils.gender_enum import GenderEnum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class ReadTaskUseCase:
    def _extract_face_schema(self, face: FaceModel) -> FaceSchema:
        bbox_schema = BoundingBox(
            height=face.bbox_height,
            width=face.bbox_width,
            x=face.bbox_x,
            y=face.bbox_y,
        )
        face_schema = FaceSchema(
            bbox=bbox_schema,
            gender=face.gender,
            age=face.age,
        )
        return face_schema

    async def execute(
        self,
        id: UUID,
        session: AsyncSession,
    ) -> TaskSchema:
        task_model = await session.get(
            TaskModel,
            id,
            options=(selectinload(TaskModel.images).selectinload(ImageModel.faces),),
        )

        image_schemas = []
        all_faces = []

        for image in task_model.images:
            image: ImageModel

            image_schema = ImageSchema(
                name=image.name,
                faces=[],
            )
            image_schemas.append(image_schema)
            for face in image.faces:
                face_schema = self._extract_face_schema(face)
                image_schema.faces.append(face_schema)
                all_faces.append(face_schema)

        males = list(filter(lambda x: x.gender.value == GenderEnum.MALE, all_faces))
        females = list(
            filter(lambda x: x.gender.value == GenderEnum.FEMALE, all_faces),
        )
        task_schema = TaskSchema(
            id=str(task_model.id),
            images=image_schemas,
            total_faces=len(all_faces),
            total_males=len(males),
            total_females=len(females),
            average_male_age=mean(face.age for face in males) if males else 0,
            average_female_age=mean(face.age for face in females) if females else 0,
        )
        return task_schema
