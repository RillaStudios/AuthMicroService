from typing import Optional

from fastapi import APIRouter
from starlette.responses import Response

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/")
async def get_user():
    return {"message": "Get all users"}

@user_router.get("/{uid}")
async def get_user_by_id(uid):

    if not isinstance(uid, int) or uid is None:
        return Response(status_code=400, content="Invalid user ID")

    else:
        return {"message": f"Get user with ID {uid}"}