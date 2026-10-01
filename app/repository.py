from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Consulta

def listar_consultas(db: Session, limite: int = 50, offset: int = 0) -> list[Consulta]:
    query = (
        select(Consulta)
        .order_by(Consulta.data_consulta.desc(), Consulta.id.desc())
        .limit(limite)
        .offset(offset) #quantos registros pular
    )
    return list(db.scalars(query).all())


def salvar_consulta(db: Session, endereco: dict) -> Consulta:
    consulta = Consulta(**endereco)
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta

