from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Путь к базе данных (параметры подключения)
SQLALCHEMY_DATABASE_URL = "postgresql://perpl:123456@localhost:5432/lsma"

# Создаем движок базы данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем сиссию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Определяем базовый класс
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
