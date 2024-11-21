# Хранилище активных WebSocket-подключений
from typing import Dict, List
from fastapi import WebSocket


active_connections: Dict[str, Dict[str, List[WebSocket]]] = {}

