import httpx

VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"
TIMEOUT_SEGUNDOS = 5.0


class CepNaoEncontradoError(Exception):
    """O ViaCEP não conhece esse CEP."""


class ViaCepIndisponivelError(Exception):
    """Falha ao comunicar com o ViaCEP (rede, timeout ou erro do servidor)."""

#requisição assincrona do viacep
async def buscar_endereco(cep: str) -> dict:
    url = VIACEP_URL.format(cep=cep)

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SEGUNDOS) as client:
            resposta = await client.get(url)
            resposta.raise_for_status()
    except httpx.HTTPError as erro:
        raise ViaCepIndisponivelError(str(erro)) from erro

    dados = resposta.json()

    if dados.get("erro"):
        raise CepNaoEncontradoError(cep)

    return {
        "cep": cep,
        "logradouro": dados.get("logradouro", ""),
        "bairro": dados.get("bairro", ""),
        "cidade": dados.get("localidade", ""),
    }