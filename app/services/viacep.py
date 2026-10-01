import logging

import httpx

logger = logging.getLogger(__name__)

VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"
TIMEOUT_SEGUNDOS = 5.0


class CepNaoEncontradoError(Exception):
    """O ViaCEP não conhece esse CEP."""


class ViaCepIndisponivelError(Exception):
    """Falha ao comunicar com o ViaCEP (rede ou erro do servidor)."""


class ViaCepTimeoutError(ViaCepIndisponivelError):
    """O ViaCEP demorou demais para responder."""


class ViaCepRespostaInvalidaError(ViaCepIndisponivelError):
    """O ViaCEP respondeu algo que não conseguimos interpretar."""

#requisição assincrona do via cep
async def buscar_endereco(cep: str) -> dict:
    url = VIACEP_URL.format(cep=cep)

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SEGUNDOS) as client:
            resposta = await client.get(url)
            resposta.raise_for_status()
    except httpx.TimeoutException as erro:
        logger.error("Timeout ao consultar o ViaCEP (cep=%s)", cep)
        raise ViaCepTimeoutError(str(erro)) from erro
    except httpx.HTTPError as erro:
        logger.error("Falha ao consultar o ViaCEP (cep=%s): %s", cep, erro)
        raise ViaCepIndisponivelError(str(erro)) from erro

    try:
        dados = resposta.json()
    except ValueError as erro:
        logger.error("Resposta do ViaCEP não é JSON (cep=%s)", cep)
        raise ViaCepRespostaInvalidaError("Resposta não é JSON válido") from erro

    if not isinstance(dados, dict):
        logger.error("Formato inesperado na resposta do ViaCEP (cep=%s)", cep)
        raise ViaCepRespostaInvalidaError("Formato de resposta inesperado")

    if dados.get("erro"):
        logger.warning("CEP não encontrado (cep=%s)", cep)
        raise CepNaoEncontradoError(cep)

    return {
        "cep": cep,
        "logradouro": dados.get("logradouro", ""),
        "bairro": dados.get("bairro", ""),
        "cidade": dados.get("localidade", ""),
    }