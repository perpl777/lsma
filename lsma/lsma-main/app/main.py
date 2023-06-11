from fastapi import FastAPI
from . import models
from .database import engine
from .routes import post


app = FastAPI()

# Создаем таблицы в PostgreSQL.
# Если они уже созданы, то ничего не произойдет.
models.Base.metadata.create_all(bind=engine)

# Подключаем объект router из файла post
app.include_router(post.router)
# app.include_router(user.router)



@app.get("/")
def root():
    return {"message": "hello"}
