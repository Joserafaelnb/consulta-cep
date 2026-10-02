import asyncio

import httpx
import pytest

from app.services.viacep import (
    CepNaoEncontradoError,
    ViaCepIndisponivelError,
    ViaCepRespostaInvalidaError,
    ViaCepTimeoutError,
    buscar_endereco,
)


def simular_viacep(monkeypatch, handler):
    """Faz o httpx responder com `handler` em vez de acessar a internet."""
    cliente_original = httpx.AsyncClient

    def cliente_falso(*args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(handler)
        return cliente_original(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", cliente_falso)


def test_mapeia_localidade_para_cidade(monkeypatch):
    def handler(request):
        return httpx.Response(
            200,
            json={
                "cep": "01001-000",
                "logradouro": "Praça da Sé",
                "bairro": "Sé",
                "localidade": "São Paulo",
                "uf": "SP",
            },
        )

    simular_viacep(monkeypatch, handler)

    endereco = asyncio.run(buscar_endereco("01001000"))

    assert endereco == {
        "cep": "01001000",
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "cidade": "São Paulo",
    }


def test_cep_geral_sem_logradouro(monkeypatch):
    simular_viacep(
        monkeypatch,
        lambda request: httpx.Response(200, json={"localidade": "Natal"}),
    )

    endereco = asyncio.run(buscar_endereco("59000000"))

    assert endereco["logradouro"] == ""
    assert endereco["cidade"] == "Natal"


def test_cep_inexistente_levanta_erro(monkeypatch):
    simular_viacep(
        monkeypatch, lambda request: httpx.Response(200, json={"erro": True})
    )

    with pytest.raises(CepNaoEncontradoError):
        asyncio.run(buscar_endereco("99999999"))


def test_timeout_levanta_erro_especifico(monkeypatch):
    def handler(request):
        raise httpx.ConnectTimeout("demorou", request=request)

    simular_viacep(monkeypatch, handler)

    with pytest.raises(ViaCepTimeoutError):
        asyncio.run(buscar_endereco("01001000"))


def test_erro_500_do_viacep(monkeypatch):
    simular_viacep(monkeypatch, lambda request: httpx.Response(500))

    with pytest.raises(ViaCepIndisponivelError):
        asyncio.run(buscar_endereco("01001000"))


def test_resposta_que_nao_e_json(monkeypatch):
    simular_viacep(
        monkeypatch, lambda request: httpx.Response(200, text="<html>erro</html>")
    )

    with pytest.raises(ViaCepRespostaInvalidaError):
        asyncio.run(buscar_endereco("01001000"))


def test_json_com_formato_inesperado(monkeypatch):
    simular_viacep(monkeypatch, lambda request: httpx.Response(200, json=[1, 2, 3]))

    with pytest.raises(ViaCepRespostaInvalidaError):
        asyncio.run(buscar_endereco("01001000"))