from sqlalchemy.ext.asyncio import AsyncSession


class ProjectsRepository:
    def __init__(self, db: AsyncSession):
        self.projects_repository = ProjectsRepository(db)
