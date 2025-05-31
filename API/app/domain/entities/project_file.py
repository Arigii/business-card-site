from pydantic import BaseModel


class ProjectFileEntity(BaseModel):
    id: int
    filename: str
    file_path: str
    project_id: int
