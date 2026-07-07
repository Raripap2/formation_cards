'''from datetime import datetime, timedelta
from typing import Optional, Dict

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError as JWTError
from pydantic import BaseModel

from utils.subprocess import workers_db

# Глобальное хранилище активных сессий
ACTIVE_SESSIONS = {}  # Формат: {worker_id: {"params": Dict, "last_active": datetime}}

#auth_router = APIRouter(prefix="/auth", tags=["Auth"])

# Конфиг JWT
SECRET_KEY = "your-secret-key"  # Замените в продакшене!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Модели
class User(BaseModel):
    worker_id: str
    params: Dict  # Параметры сессии


class Token(BaseModel):
    access_token: str
    token_type: str


# Зависимость для проверки БД (ЗАМЕНИТЕ НА СВОЮ ФУНКЦИЮ!)
async def verify_user_in_db(worker_id: str, password: str) -> Optional[Dict]:
    """Возвращает params пользователя, если логин/пароль верные, иначе None."""
    worker = workers_db.get(
        fields=['worker_id', 'status_id'],
        order_by='worker_id',
        order_direction='ASC',
        filters={
            'login': login,
            'hash_password': password
        }
    )
    if worker:
        return {'worker_id': worker[0]['worker_id'], 'status_id': worker[0]['status_id']}
    return None


# Генерация JWT
def create_access_token(data: dict) -> str:
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expires})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# Проверка токена и сессии
async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/token"))) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        worker_id = payload.get("sub")
        if not worker_id or worker_id not in ACTIVE_SESSIONS:
            raise HTTPException(status_code=401, detail="Invalid or expired session")

        # Обновляем время активности
        ACTIVE_SESSIONS[worker_id]["last_active"] = datetime.utcnow()
        return User(worker_id=worker_id, params=ACTIVE_SESSIONS[worker_id]["params"])

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Роуты
@auth_router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_params = await verify_user_in_db(form_data.username, form_data.password)
    if not user_params:
        raise HTTPException(status_code=400, detail="Incorrect worker_id or password")

    worker_id = form_data.username
    ACTIVE_SESSIONS[worker_id] = {
        "params": user_params,
        "last_active": datetime.utcnow()
    }

    token = create_access_token({"sub": worker_id})
    return {"access_token": token, "token_type": "bearer"}


@auth_router.get("/me", response_model=User)
async def read_current_user(user: User = Depends(get_current_user)):
    return user
'''