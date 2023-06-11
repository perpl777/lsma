# APIRouter нужен, чтобы получить доступ к объекту app из файла main.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from typing import List

router = APIRouter(
    prefix="/posts"
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return posts

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session=Depends(get_db)):

    # Вместо .all() тут будет использоваться .first(), так как
    # мы точно знаем, что запись с требуемым id будет только одна,
    # а значит, нет никакого смысла искать дальше.
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found")

    return post

@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session=Depends(get_db)):

    # Создаем новый объект
    new_post = models.Post(**post.dict())

    # Добавляем его в базу данных
    db.add(new_post)

    # Записываем изменения
    db.commit()

    # Получаем созданный объект (аналог RETURNING).
    # Он запишется в переменную new_post.
    db.refresh(new_post)

    return new_post

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

@router.delete("/{id}")
def delete_post(id: int, db: Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


