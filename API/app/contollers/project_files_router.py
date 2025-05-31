from fastapi import Depends, File, UploadFile, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from app.database.session import get_db
from app.domain.entities.project_file import ProjectFileEntity
from app.infrastructure.dependencies import get_current_user, require_admin
from app.infrastructure.project_files_service import ProjectFilesService

router = APIRouter()


@router.get(
    "/projects/{project_id}/",
    response_model=list[ProjectFileEntity],
    summary="Get all project files",
    description="Returns metadata of all files uploaded for the specified project."
)
async def get_files_by_project_id(
        project_id: int,
        db: AsyncSession = Depends(get_db),
):
    service = ProjectFilesService(db)
    return await service.get_files_by_project_id(project_id)


@router.get(
    "/{file_id}/file",
    response_class=FileResponse,
    summary="Download project file by ID",
    description="Returns the file for the specified file ID."
)
async def download_project_file(
        file_id: int,
        db: AsyncSession = Depends(get_db),
):
    service = ProjectFilesService(db)
    return await service.get_file_by_id(file_id)


@router.post(
    "/projects/{project_id}/upload",
    response_model=ProjectFileEntity,
    summary="Upload a new file for the project",
    description="Uploads a new file and associates it with the specified project."
)
async def upload_project_file(
        project_id: int,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    service = ProjectFilesService(db)
    return await service.upload_file(project_id, file, user)


@router.delete(
    "/{file_id}/",
    response_model=ProjectFileEntity,
    summary="Delete a project file by ID",
    description="Deletes the file and its database entry."
)
async def delete_project_file(
        file_id: int,
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    service = ProjectFilesService(db)
    return await service.delete_file(file_id, user)
