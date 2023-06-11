from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str


class Post(PostBase):
    id: int
    created_at: datetime

    # Чтобы pydantic мог сериализовать orm-модель, нужно
    # добавить такой конфиг
    class Config:
        orm_mode = True

class PostCreate(PostBase):
    published: bool = True
