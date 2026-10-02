from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Consulta


def salvar_consulta(db: Session, endereco: dict, visitor_id: str) -> Consulta:
    consulta = Consulta(**endereco, visitor_id=visitor_id)
    db.add(consulta)
    try:
        db.commit()
    except SQLAlchemyError: #desfaz a consulta
        db.rollback()
        raise
    db.refresh(consulta)
    return consulta


def listar_consultas(db: Session, limite: int = 50, offset: int = 0) -> list[Consulta]:
    query = (
        select(Consulta)
        .order_by(Consulta.data_consulta.desc(), Consulta.id.desc())
        .limit(limite)
        .offset(offset) #pula consultas
    )
    return list(db.scalars(query).all())


def listar_consultas_do_visitante(
    db: Session, visitor_id: str, limite: int, offset: int
) -> list[Consulta]:
    query = (
        select(Consulta)
        .where(Consulta.visitor_id == visitor_id)
        .order_by(Consulta.data_consulta.desc(), Consulta.id.desc())
        .limit(limite)
        .offset(offset)
    )
    return list(db.scalars(query).all())


def contar_consultas_do_visitante(db: Session, visitor_id: str) -> int:
    query = (
        select(func.count())
        .select_from(Consulta)
        .where(Consulta.visitor_id == visitor_id)
    )
    return db.scalar(query) or 0