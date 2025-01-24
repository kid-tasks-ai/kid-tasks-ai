from fastapi import APIRouter

# from app.api.v1.auth import router as auth_router
# from app.api.v1.children import router as children_router
# from app.api.v1.tasks import router as tasks_router
# from app.api.v1.rewards import router as rewards_router

from app.api.v1 import (
    auth,
    children,
    rewards,
    tasks,
    me
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(children.router, prefix="/children", tags=["children"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(rewards.router, prefix="/rewards", tags=["rewards"])
api_router.include_router(me.router, prefix="/me", tags=["rewards"])
