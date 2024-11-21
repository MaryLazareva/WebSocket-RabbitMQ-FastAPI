from fastapi import APIRouter
from datetime import datetime, timedelta
import jwt
from app.config import SECRET_KEY, ALGORITHM
from app.schemas import TokenRequest

router = APIRouter()

# Эндпоинт для генерации токена
@router.post("/generate-token")
async def generate_token(data: TokenRequest):
    """Генерация токена с указанием комнаты"""
    payload = {
        "username": data.username,
        "email": data.email,
        "room_id": data.room_id,
        "exp": datetime.now() + timedelta(hours=1),  # Токен действует 1 час
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # Шифрование словаря в jwt-токен
    return {"token": token}
