from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import settings
from app.database.session import init_db


def create_app() -> FastAPI:
    api = FastAPI(
        title=settings.app_name,
        description="Intelligent resume screening and candidate ranking API.",
        version="0.1.0",
    )

    api.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @api.on_event("startup")
    def on_startup() -> None:
        init_db()

    api.include_router(router)
    return api


app = create_app()
