from fastapi import Depends, File, UploadFile, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from app.database.session import get_db
from app.domain.entities.profile_photo import ProfilePhotoEntity
from app.infrastructure.dependencies import get_current_user, require_admin
from app.infrastructure.profile_photos_service import ProfilePhotosService

router = APIRouter()


@router.get(
    "/profiles/{profile_id}/",
    response_model=list[ProfilePhotoEntity],
    summary="Get all photos metadata for a profile",
    description="Returns metadata of all profile photos for the given profile_id",
)
async def get_photos_by_profile_id(
        profile_id: int,
        db: AsyncSession = Depends(get_db),
):
    service = ProfilePhotosService(db)
    return await service.get_photo_file_by_profile_id(profile_id)


@router.get(
    "/{photo_id}/file",
    response_class=FileResponse,
    summary="Download photo file by photo ID",
    description="Returns the image file for the given photo ID",
)
async def download_photo_file(
        photo_id: int,
        db: AsyncSession = Depends(get_db),
):
    service = ProfilePhotosService(db)
    return await service.get_photo_file_by_id(photo_id)


@router.post(
    "/profiles/{profile_id}/upload",
    response_model=ProfilePhotoEntity,
    summary="Upload a new photo for a profile",
    description="Uploads a new photo file and associates it with the given profile ID",
)
async def upload_photo(
        profile_id: int,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user),
):
    service = ProfilePhotosService(db)
    return await service.upload_photo(profile_id, file, user)


@router.delete(
    "/{photo_id}/",
    response_model=ProfilePhotoEntity,
    summary="Delete a photo by ID",
    description="Deletes a photo and its file from storage",
)
async def delete_photo(
        photo_id: int,
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user),
):
    service = ProfilePhotosService(db)
    return await service.delete_photo(photo_id, user)
