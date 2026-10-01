from sqlalchemy.orm import Session

from app.models import Consulta


def salvar_consulta(db: Session, endereco: dict) -> Consulta:
    consulta = Consulta(**endereco)
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta