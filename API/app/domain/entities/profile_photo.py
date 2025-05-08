from pydantic import BaseModel


class ProfilePhotoEntity(BaseModel):
    id: int
    filename: str
    file_path: str
    profile_id: int
