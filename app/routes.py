from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import listar_consultas, salvar_consulta
from app.schemas import ConsultaRequest, ConsultaResponse
from app.services.viacep import (
    CepNaoEncontradoError,
    ViaCepIndisponivelError,
    buscar_endereco,
)

router = APIRouter(prefix="/consultas", tags=["Consultas"])

#esta rota faz uma consulta com o viacerta, utiliza o schema para validar o cep, e retorna um json com o formato esperado tratando erros
@router.post("", response_model=ConsultaResponse)
async def consultar_cep(dados: ConsultaRequest, db: Session = Depends(get_db)):
    try:
        endereco = await buscar_endereco(dados.cep)
    except CepNaoEncontradoError:
        raise HTTPException(status_code=404, detail="CEP não encontrado")
    except ViaCepIndisponivelError:
        raise HTTPException(
            status_code=502, detail="Serviço de consulta de CEP indisponível"
        )

    return salvar_consulta(db, endereco)


#essa rota retorna dados de tabelas salvas no banco 
@router.get("", response_model=list[ConsultaResponse])
def listar_historico(
    limite: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return listar_consultas(db, limite, offset)