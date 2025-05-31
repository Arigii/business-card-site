import os
import uuid

import aiofiles
import magic
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse
from werkzeug.utils import secure_filename

from app.application.project_files_repository import ProjectFilesRepository
from app.application.projects_repository import ProjectsRepository
from app.domain.entities.project_file import ProjectFileEntity
from app.domain.models import ProjectFile, User


class ProjectFilesService:
    def __init__(self, db: AsyncSession):
        self.project_files_repository = ProjectFilesRepository(db)
        self.projects_repository = ProjectsRepository(db)

    async def get_file_by_id(self, file_id: int) -> FileResponse:
        project_file = await self.project_files_repository.get_by_id(file_id)

        if not project_file:
            raise HTTPException(404, "File not found")

        if not os.path.exists(project_file.file_path):
            raise HTTPException(404, "File not found on disk")

        return FileResponse(
            project_file.file_path,
            media_type=self.get_media_type(project_file.file_path),
            filename=os.path.basename(project_file.file_path),
        )

    async def get_files_by_project_id(self, project_id: int) -> list[ProjectFileEntity]:
        files = await self.project_files_repository.get_by_project_id(project_id)
        return [self.model_to_entity(file) for file in files]

    async def upload_file(self, project_id: int, file: UploadFile, user: User) -> ProjectFileEntity:
        project = await self.projects_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(404, "Project not found")

        self.validate_file_type(file)
        file_path = await self.save_file(file)

        project_file = ProjectFile(
            filename=file.filename,
            file_path=file_path,
            project_id=project_id,
        )

        return self.model_to_entity(
            await self.project_files_repository.create(project_file)
        )

    async def delete_file(self, file_id: int, user: User) -> ProjectFileEntity:
        project_file = await self.project_files_repository.get_by_id(file_id)
        if not project_file:
            raise HTTPException(404, "File not found")

        if os.path.exists(project_file.file_path):
            os.remove(project_file.file_path)

        return self.model_to_entity(
            await self.project_files_repository.delete(project_file)
        )

    async def save_file(self, file: UploadFile, upload_dir: str = "uploads/project_files") -> str:
        os.makedirs(upload_dir, exist_ok=True)
        filename = self.generate_filename(file)
        file_path = os.path.join(upload_dir, filename)

        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        return file_path

    @staticmethod
    def validate_file_type(file: UploadFile):
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(file.file.read(1024))
        file.file.seek(0)

        allowed_types = [
            "application/pdf",
            "image/jpeg",
            "image/png",
            "application/zip",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "text/plain",
        ]

        if file_type not in allowed_types:
            raise HTTPException(400, f"Invalid file type: {file_type}")

    @staticmethod
    def generate_filename(file: UploadFile) -> str:
        return secure_filename(f"{uuid.uuid4()}_{file.filename}")

    @staticmethod
    def model_to_entity(project_file_model: ProjectFile) -> ProjectFileEntity:
        return ProjectFileEntity(
            id=project_file_model.id,
            filename=project_file_model.filename,
            file_path=project_file_model.file_path,
            project_id=project_file_model.project_id,
        )

    @staticmethod
    def get_media_type(filename: str) -> str:
        extension = filename.split('.')[-1].lower()
        if extension in ['jpeg', 'jpg', 'png']:
            return f"image/{extension}"
        if extension == 'pdf':
            return "application/pdf"
        if extension in ['zip']:
            return "application/zip"
        if extension in ['doc', 'docx']:
            return "application/msword"
        if extension in ['xls', 'xlsx']:
            return "application/vnd.ms-excel"
        if extension in ['ppt', 'pptx']:
            return "application/vnd.ms-powerpoint"
        if extension in ['txt']:
            return "text/plain"
        return "application/octet-stream"
