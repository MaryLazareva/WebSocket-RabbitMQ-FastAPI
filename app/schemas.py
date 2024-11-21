from pydantic import BaseModel

class Message(BaseModel):
    room_id: str
    content: str

class User(BaseModel):
    username: str
    email: str

class TokenRequest(BaseModel):
    username: str
    email: str
    room_id: str
