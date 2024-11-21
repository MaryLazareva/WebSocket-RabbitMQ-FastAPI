from fastapi import FastAPI
from app.routers import auth, websocket, messages

app = FastAPI()

# Подключаем маршруты
app.include_router(auth.router)
app.include_router(websocket.router)
app.include_router(messages.router)
