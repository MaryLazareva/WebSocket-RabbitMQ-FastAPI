from fastapi import APIRouter
from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit import RabbitQueue
from app.schemas import Message
from app.storage import active_connections


router = RabbitRouter("amqp://guest:guest@localhost:5672/") # RabbitRouter управляет очередями и публикацией/подпиской на сообщения


# Эндпоинт для публикации сообщений
@router.post("/message")
async def post_message(message: Message):
    room_id = message.room_id
    # Общая очередь для подписки на все сообщения
    messages_queue = RabbitQueue(name="messages")

    try:
        # Объявление общей очереди (если не существует)
        await router.broker.declare_queue(messages_queue)

        # Публикация сообщения в очередь messages
        await router.broker.publish(message.model_dump(), queue=messages_queue.name)

        return {"status": f"Message sent to room: {room_id}"}
    except Exception as e:
        # Логирование и возвращение ошибки
        print(f"Failed to send message to room: {room_id}: {e}")
        return {"status": "error", "detail": str(e)}


# Подписчик на очередь
@router.subscriber(queue="messages")
async def message_handler(message: dict):
    room_id = message.get("room_id")
    if not room_id:
        return
    
    print(f"Received message for room: {room_id} - {message}")
    if room_id in active_connections:
        for username, connections in active_connections[room_id].items():
            for client in connections:
                try:
                    await client.send_text(message.get("content", ""))  # Отправка текста всем соединениям пользователя
                except Exception as e:
                    print(f"Failed to send message to client in room {room_id}: {e}")



