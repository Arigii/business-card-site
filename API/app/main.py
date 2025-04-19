from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def start_app():
    api_app = FastAPI()

    api_app.add_middleware(
        CORSMiddleware,
        allow_origins=["http//localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return api_app

app = start_app()

@app.get("/")
async def root():
    return {"message": "Hello API"}