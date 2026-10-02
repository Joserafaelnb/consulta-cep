from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Consulta(Base):
    __tablename__ = "consultas"

    id: Mapped[int] = mapped_column(primary_key=True)
    cep: Mapped[str] = mapped_column(String(8), index=True)
    logradouro: Mapped[str]
    bairro: Mapped[str]
    cidade: Mapped[str]
    visitor_id: Mapped[str] = mapped_column(String(36), index=True)
    data_consulta: Mapped[datetime] = mapped_column(default=datetime.now)