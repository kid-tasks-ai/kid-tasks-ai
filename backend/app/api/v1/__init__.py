from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.children import router as children_router
from app.api.v1.tasks import router as tasks_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(children_router, prefix="/children", tags=["children"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
