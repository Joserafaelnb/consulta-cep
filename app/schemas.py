from datetime import datetime

from pydantic import BaseModel, field_validator


#classe de regra de negocio responsavel por fazer uma requisição e validar os dados
class ConsultaRequest(BaseModel):
    cep: str

    @field_validator("cep")
    @classmethod
    def validar_cep(cls, valor: str) -> str:
        apenas_digitos = valor.replace("-", "").strip()
        if not (apenas_digitos.isdigit() and len(apenas_digitos) == 8):
            raise ValueError("CEP deve conter exatamente 8 dígitos numéricos")
        return apenas_digitos


#classe de regra de negocio responsavel por entregar uma requisição no formato correto
class ConsultaResponse(BaseModel):
    cep: str
    logradouro: str
    bairro: str
    cidade: str
    dataConsulta: datetime