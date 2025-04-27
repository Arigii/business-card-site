from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.contollers.register_controller import router as register_router
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

    return api_app


app = start_app()


@app.get("/")
async def root():
    return {"message": "Hello API"}
