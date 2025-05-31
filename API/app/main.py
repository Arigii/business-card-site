from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.contollers.auth_router import router as auth_router
from app.contollers.profile_photos_router import router as profile_photos_router
from app.contollers.profiles_router import router as profiles_router
from app.contollers.project_files_router import router as project_files_router
from app.contollers.project_members_router import router as project_members_router
from app.contollers.projects_router import router as projects_router
from app.contollers.register_router import router as register_router
from app.contollers.teams_router import router as team_router
from app.contollers.users_router import router as users_router
from app.settings import settings


def start_app():
    api_app = FastAPI()

    api_app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_app.include_router(auth_router, prefix=f'{settings.PREFIX}/auth', tags=['auth'])
    api_app.include_router(profile_photos_router, prefix=f'{settings.PREFIX}/profile_photos', tags=['profile_photos'])
    api_app.include_router(profiles_router, prefix=f'{settings.PREFIX}/profiles', tags=['profiles'])
    api_app.include_router(project_files_router, prefix=f'{settings.PREFIX}/project_files', tags=['project_files'])
    api_app.include_router(project_members_router, prefix=f'{settings.PREFIX}/project_members', tags=['project_members'])
    api_app.include_router(projects_router, prefix=f'{settings.PREFIX}/projects', tags=['projects'])
    api_app.include_router(register_router, prefix=f'{settings.PREFIX}/register', tags=['register'])
    api_app.include_router(team_router, prefix=f'{settings.PREFIX}/teams', tags=['teams'])
    api_app.include_router(users_router, prefix=f'{settings.PREFIX}/users', tags=['users'])

    return api_app


app = start_app()


@app.get("/")
async def root():
    return {"message": "Hello API"}
