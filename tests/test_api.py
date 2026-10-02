import pytest
from sqlalchemy import select

from app.models import Consulta
from app.services.viacep import (
    CepNaoEncontradoError,
    ViaCepIndisponivelError,
    ViaCepTimeoutError,
)


def contar_consultas(db_session) -> int:
    return len(db_session.scalars(select(Consulta)).all())


@pytest.fixture
def viacep_ok(monkeypatch):
    async def falso(cep):
        return {
            "cep": cep,
            "logradouro": "Praça da Sé",
            "bairro": "Sé",
            "cidade": "São Paulo",
        }

    monkeypatch.setattr("app.routes.buscar_endereco", falso)


def simular_falha(monkeypatch, excecao):
    async def falso(cep):
        raise excecao

    monkeypatch.setattr("app.routes.buscar_endereco", falso)


def test_consulta_com_sucesso(client, db_session, viacep_ok):
    resposta = client.post("/api/consultas", json={"cep": "01001000"})

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["cep"] == "01001000"
    assert corpo["logradouro"] == "Praça da Sé"
    assert corpo["cidade"] == "São Paulo"
    assert "dataConsulta" in corpo
    assert contar_consultas(db_session) == 1


def test_cep_com_hifen_e_normalizado(client, viacep_ok):
    resposta = client.post("/api/consultas", json={"cep": "01001-000"})

    assert resposta.status_code == 200
    assert resposta.json()["cep"] == "01001000"


@pytest.mark.parametrize(
    "cep",
    [
        "abc",
        "123",
        "",
        "1; DROP TABLE consultas;--",
        "５９０００００００",
        "5-9-0-0-0-0-0-0",
        "0100100000",
    ],
)
def test_cep_invalido_retorna_422(client, db_session, viacep_ok, cep):
    resposta = client.post("/api/consultas", json={"cep": cep})

    assert resposta.status_code == 422
    assert contar_consultas(db_session) == 0


def test_cep_nao_encontrado_retorna_404(client, db_session, monkeypatch):
    simular_falha(monkeypatch, CepNaoEncontradoError("99999999"))

    resposta = client.post("/api/consultas", json={"cep": "99999999"})

    assert resposta.status_code == 404
    assert contar_consultas(db_session) == 0


def test_timeout_do_viacep_retorna_504(client, db_session, monkeypatch):
    simular_falha(monkeypatch, ViaCepTimeoutError("timeout"))

    resposta = client.post("/api/consultas", json={"cep": "01001000"})

    assert resposta.status_code == 504
    assert contar_consultas(db_session) == 0


def test_viacep_indisponivel_retorna_502(client, db_session, monkeypatch):
    simular_falha(monkeypatch, ViaCepIndisponivelError("fora do ar"))

    resposta = client.post("/api/consultas", json={"cep": "01001000"})

    assert resposta.status_code == 502
    assert contar_consultas(db_session) == 0


def test_historico_vazio(client):
    resposta = client.get("/api/consultas")

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_historico_ordenado_do_mais_recente_e_com_id(client, viacep_ok):
    client.post("/api/consultas", json={"cep": "01001000"})
    client.post("/api/consultas", json={"cep": "20040020"})

    itens = client.get("/api/consultas").json()

    assert [i["cep"] for i in itens] == ["20040020", "01001000"]
    assert all("id" in i and "dataConsulta" in i for i in itens)


def test_historico_paginacao(client, viacep_ok):
    for cep in ["01001000", "20040020", "30140071"]:
        client.post("/api/consultas", json={"cep": cep})

    pagina1 = client.get("/api/consultas?limite=2").json()
    pagina2 = client.get("/api/consultas?limite=2&offset=2").json()

    assert len(pagina1) == 2
    assert [i["cep"] for i in pagina2] == ["01001000"]


@pytest.mark.parametrize("query", ["limite=0", "limite=201", "offset=-1"])
def test_historico_parametros_invalidos(client, query):
    assert client.get(f"/api/consultas?{query}").status_code == 422


def test_rate_limit_bloqueia_a_11a_requisicao(client, viacep_ok):
    for _ in range(10):
        assert client.post("/api/consultas", json={"cep": "01001000"}).status_code == 200

    resposta = client.post("/api/consultas", json={"cep": "01001000"})

    assert resposta.status_code == 429


def test_headers_de_seguranca(client):
    resposta = client.get("/health")

    assert resposta.headers["X-Content-Type-Options"] == "nosniff"
    assert resposta.headers["X-Frame-Options"] == "DENY"