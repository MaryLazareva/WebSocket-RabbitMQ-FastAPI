from fastapi import HTTPException, status, WebSocket
import jwt
from app.config import SECRET_KEY, ALGORITHM
from app.schemas import User

# Функция для извлечения пользователя из токена
async def get_user_from_token(websocket: WebSocket) -> User:
    """Извлечение информации о пользователе из токена (JWT)"""
    # Извлечение токена из заголовков WebSocket
    token = websocket.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token"
        )

    token = token.split(" ")[1]  # Убираем "Bearer" из токена

    try:
        # Расшифровка токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return User(username=payload["username"], email=payload["email"], room_id=payload["room_id"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    

    