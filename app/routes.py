import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.limiter import limiter

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import listar_consultas, salvar_consulta
from app.schemas import ConsultaRequest, ConsultaResponse, HistoricoResponse
from app.services.viacep import (
    CepNaoEncontradoError,
    ViaCepIndisponivelError,
    ViaCepTimeoutError,
    buscar_endereco,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/consultas", tags=["Consultas"])

#esta rota faz uma consulta com o viacerta, utiliza o schema para validar o cep, e retorna um json com o formato esperado tratando erros
@router.post("", response_model=ConsultaResponse)
@limiter.limit("10/minute")
async def consultar_cep(
    request: Request, dados: ConsultaRequest, db: Session = Depends(get_db)
):
    try:
        endereco = await buscar_endereco(dados.cep)
    except CepNaoEncontradoError:
        raise HTTPException(status_code=404, detail="CEP não encontrado")
    except ViaCepTimeoutError:
        raise HTTPException(
            status_code=504, detail="O serviço de CEP demorou demais para responder"
        )
    except ViaCepIndisponivelError:
        raise HTTPException(
            status_code=502, detail="Serviço de consulta de CEP indisponível"
        )

#trata erros ao tentar salvar no banco de dados
    try:
        consulta = salvar_consulta(db, endereco)
    except SQLAlchemyError:
        logger.exception("Falha ao gravar consulta (cep=%s)", dados.cep)
        raise HTTPException(status_code=500, detail="Erro ao salvar a consulta")

    logger.info("Consulta realizada (cep=%s)", dados.cep)
    return consulta


#essa rota retorna dados de tabelas salvas no banco 
@router.get("", response_model=list[HistoricoResponse])
def listar_historico(
    limite: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return listar_consultas(db, limite, offset)