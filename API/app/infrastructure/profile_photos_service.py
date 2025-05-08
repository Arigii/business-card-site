import os
import uuid

import aiofiles
import magic

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse
from werkzeug.utils import secure_filename

from app.application.profile_photos_repository import ProfilePhotosRepository
from app.application.users_repository import UsersRepository
from app.domain.entities.profile_photo import ProfilePhotoEntity
from app.domain.models import ProfilePhoto, User


class ProfilePhotosService:
    def __init__(self, db: AsyncSession):
        self.profile_photos_repository = ProfilePhotosRepository(db)
        self.users_repository = UsersRepository(db)

    async def get_photo_file_by_id(self, photo_id: int) -> FileResponse:
        photo = await self.profile_photos_repository.get_by_id(photo_id)

        if not photo:
            raise HTTPException(404, "Photo not found")

        if not os.path.exists(photo.file_path):
            raise HTTPException(404, "File not found on disk")

        return FileResponse(
            photo.file_path,
            media_type=self.get_media_type(photo.filename),
            filename=photo.filename,
        )

    async def get_photo_file_by_profile_id(self, profile_id: int) -> list[ProfilePhotoEntity]:
        photos = await self.profile_photos_repository.get_by_profile_id(profile_id)
        return [
            self.model_to_entity(photo)
            for photo in photos
        ]

    async def upload_photo(self, profile_id: int, file: UploadFile, user: User):
        user = await self.users_repository.get_by_id(user.id)

        if profile_id != user.profile_id and user.profile.role.title != 'Администратор':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        self.validate_file_type(file)

        photo = ProfilePhoto(
            filename=self.generate_filename(file),
            file_path=await self.save_file(file),
            profile_id=profile_id
        )

        return self.model_to_entity(
            await self.profile_photos_repository.create(photo)
        )

    async def delete_photo(self, photo_id: int, user: User) -> ProfilePhotoEntity:
        user = await self.users_repository.get_by_id(user.id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this ID was not found",
            )

        photo = await self.profile_photos_repository.get_by_id(photo_id)
        if not photo:
            raise HTTPException(404, "Photo not found")

        if photo.profile_id != user.profile_id and user.profile.role.title != 'Администратор':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        if os.path.exists(photo.file_path):
            os.remove(photo.file_path)

        return self.model_to_entity(
            await self.profile_photos_repository.delete(photo)
        )

    async def save_file(self, file: UploadFile, upload_dir: str = "uploads/profile_photos") -> str:
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

        if file_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(400, "Invalid file type")

    @staticmethod
    def generate_filename(file: UploadFile):
        return secure_filename(f"{uuid.uuid4()}_{file.filename}")

    @staticmethod
    def model_to_entity(profile_photo_model: ProfilePhoto) -> ProfilePhotoEntity:
        return ProfilePhotoEntity(
            id=profile_photo_model.id,
            filename=profile_photo_model.filename,
            file_path=profile_photo_model.file_path,
            profile_id=profile_photo_model.profile_id,
        )

    @staticmethod
    def get_media_type(filename: str) -> str:
        extension = filename.split('.')[-1].lower()
        return f"image/{extension}" if extension in ['jpeg', 'jpg', 'png'] else "application/octet-stream"
