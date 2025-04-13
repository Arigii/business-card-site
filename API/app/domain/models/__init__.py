from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app.domain.models.contest_carousel_photos import ContestCarouselPhoto
from app.domain.models.contest_files import ContestFile
from app.domain.models.contests import Contest
from app.domain.models.contest_statuses import ContestStatus
from app.domain.models.projects import Project
from app.domain.models.project_files import ProjectFile
from app.domain.models.users import User
from app.domain.models.profiles import Profile
from app.domain.models.roles import Role
from app.domain.models.teams import Team
from app.domain.models.project_members import ProjectMember
from app.domain.models.profile_photos import ProfilePhoto
