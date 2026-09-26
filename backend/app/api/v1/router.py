from fastapi import APIRouter

api_router = APIRouter()

from app.auth.router import router as auth_router
from app.movies.router import router as movies_router

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(movies_router, prefix="/movies", tags=["movies"])