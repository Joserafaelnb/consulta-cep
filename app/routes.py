from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.schemas import ConsultaRequest, ConsultaResponse
from app.services.viacep import (
    CepNaoEncontradoError,
    ViaCepIndisponivelError,
    buscar_endereco,
)

router = APIRouter(prefix="/consultas", tags=["Consultas"])

#esta rota faz uma consulta com o viacerta, utiliza o schema para validar o cep, e retorna um json com o formato esperado tratando erros
@router.post("", response_model=ConsultaResponse)
async def consultar_cep(dados: ConsultaRequest):
    try:
        endereco = await buscar_endereco(dados.cep)
    except CepNaoEncontradoError:
        raise HTTPException(status_code=404, detail="CEP não encontrado")
    except ViaCepIndisponivelError:
        raise HTTPException(
            status_code=502, detail="Serviço de consulta de CEP indisponível"
        )

    return ConsultaResponse(**endereco, dataConsulta=datetime.now())