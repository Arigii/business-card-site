from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.contollers.register_router import router as register_router
from app.contollers.auth_router import router as auth_router
from app.contollers.teams_router import router as team_router
from app.settings import settings


def start_app():
    api_app = FastAPI()

    api_app.add_middleware(
        CORSMiddleware,
        allow_origins=["http//localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_app.include_router(register_router, prefix=f'{settings.PREFIX}/register', tags=['register'])
    api_app.include_router(auth_router, prefix=f'{settings.PREFIX}/auth', tags=['auth'])
    api_app.include_router(team_router, prefix=f'{settings.PREFIX}/teams', tags=['teams'])

    return api_app


app = start_app()


@app.get("/")
async def root():
    return {"message": "Hello API"}
