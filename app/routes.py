import logging
import uuid
from typing import Optional

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Header,
    HTTPException,
    Query,
    Request,
    Response,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.limiter import limiter
from app.repository import (
    contar_consultas_do_visitante,
    listar_consultas,
    listar_consultas_do_visitante,
    salvar_consulta,
)
from app.schemas import (
    ConsultaRequest,
    ConsultaResponse,
    HistoricoResponse,
    PaginaHistoricoResponse,
)
from app.services.viacep import (
    CepNaoEncontradoError,
    ViaCepIndisponivelError,
    ViaCepTimeoutError,
    buscar_endereco,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/consultas", tags=["Consultas"])

COOKIE_VISITANTE = "visitor_id"
UM_ANO_EM_SEGUNDOS = 60 * 60 * 24 * 365


def _visitor_id_valido(valor: Optional[str]) -> Optional[str]:
    """Aceita só UUIDs válidos; qualquer outra coisa vinda do cookie é ignorada."""
    try:
        return str(uuid.UUID(valor))
    except (ValueError, TypeError, AttributeError):
        return None

#esta rota faz uma consulta com o viacerta, utiliza o schema para validar o cep, e retorna um json com o formato esperado tratando erros
@router.post("", response_model=ConsultaResponse)
@limiter.limit("10/minute")
async def consultar_cep(
    request: Request,
    response: Response,
    dados: ConsultaRequest,
    db: Session = Depends(get_db),
    visitor_id: Optional[str] = Cookie(default=None),
    consentimento: Optional[str] = Header(default=None, alias="X-Cookie-Consent"),
):
    aceitou_cookies = consentimento == "aceito"
    if aceitou_cookies:
        visitor_id = _visitor_id_valido(visitor_id) or str(uuid.uuid4())
    else:
        visitor_id = str(uuid.uuid4())  # anônimo: ninguém vai reencontrar

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
        consulta = salvar_consulta(db, endereco, visitor_id)
    except SQLAlchemyError:
        logger.exception("Falha ao gravar consulta (cep=%s)", dados.cep)
        raise HTTPException(status_code=500, detail="Erro ao salvar a consulta")

    if aceitou_cookies:
        response.set_cookie(
            key=COOKIE_VISITANTE,
            value=visitor_id,
            max_age=UM_ANO_EM_SEGUNDOS,
            httponly=True,
            samesite="lax",
        )

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


@router.get("/minhas", response_model=PaginaHistoricoResponse)
def minhas_consultas(
    pagina: int = Query(1, ge=1),
    tamanho: int = Query(5, ge=1, le=50),
    db: Session = Depends(get_db),
    visitor_id: Optional[str] = Cookie(default=None),
):
    visitor_id = _visitor_id_valido(visitor_id)
    if visitor_id is None:
        return {"itens": [], "total": 0, "pagina": pagina, "tamanho": tamanho}

    offset = (pagina - 1) * tamanho
    return {
        "itens": listar_consultas_do_visitante(db, visitor_id, tamanho, offset),
        "total": contar_consultas_do_visitante(db, visitor_id),
        "pagina": pagina,
        "tamanho": tamanho,
    }


@router.delete("/cookie", status_code=204)
def revogar_cookie(response: Response):
    response.delete_cookie(COOKIE_VISITANTE)






