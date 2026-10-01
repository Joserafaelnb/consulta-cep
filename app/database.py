from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./consultas.db"

#cria o motor do banco de dados desabilita a limitação do sqlite de so rodar em uma thread
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

#abre uma sessão com o banco
SessionLocal = sessionmaker(bind=engine, autoflush=False)

#classe base para as outras classes
class Base(DeclarativeBase):
    pass

#função que abre a conexão com o banco e mantem aberta até a operação ser concluida
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()