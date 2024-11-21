from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.schemas import User
from app.utils.jwt_handler import get_user_from_token
from app.storage import active_connections

router = APIRouter()

# Эндпоинт подключения к комнате через WebSocket
@router.websocket("/updates/{room_id}")
async def get_updates(websocket: WebSocket, room_id: str, user: User = Depends(get_user_from_token)):
    """Подключение пользователя к комнате"""
    # Подтверждение WebSocket-соединения
    await websocket.accept()

    # Проверка или создание комнаты
    if room_id not in active_connections:
        active_connections[room_id] = {}

    room_users = active_connections[room_id]

    # Проверка на количество пользователей в комнате (не более двух уникальных пользователей)
    if len(room_users) >= 2 and user.username not in room_users:
        await websocket.close(code=4001)  
        print(f"Room: {room_id} is full. Connection denied for user: {user.username}.")
        return

    # Добавление WebSocket-соединения для пользователя
    if user.username not in room_users:
        room_users[user.username] = []
    room_users[user.username].append(websocket)

    print(f"User: {user.username} connected to room: {room_id}.")

    try:
        while True:
            await websocket.receive_text()  # Поддерживание соединения открытым
    except WebSocketDisconnect:
        # Удаление соединения при отключении
        room_users[user.username].remove(websocket)
        if not room_users[user.username]:
            del room_users[user.username]  # Удаление пользователя, если больше нет соединений
        print(f"User: {user.username} disconnected from room: {room_id}.")

        # Удаление комнаты, если больше нет пользователей
        if not room_users:
            del active_connections[room_id]
            print(f"Room: {room_id} is now empty and removed.")

