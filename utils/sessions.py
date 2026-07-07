from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.auth import ACTIVE_SESSIONS, get_current_user, User

sessions_router = APIRouter(prefix="/sessions", tags=["Sessions"])


class UpdateParamsRequest(BaseModel):
    params: Dict


@sessions_router.put("/update_params")
async def update_params(
        request: UpdateParamsRequest,
        user: User = Depends(get_current_user)
):
    if user.worker_id not in ACTIVE_SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")

    ACTIVE_SESSIONS[user.worker_id]["params"].update(request.params)
    return {"message": "Params updated", "worker_id": user.worker_id}


@sessions_router.get("/active")
async def list_active_sessions():
    return {
        "sessions": [
            {"worker_id": wid, "last_active": sess["last_active"]}
            for wid, sess in ACTIVE_SESSIONS.items()
        ]
    }
