from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

import re


#classe de regra de negocio responsavel por fazer uma requisição e validar os dados
CEP_REGEX = re.compile(r"[0-9]{5}-?[0-9]{3}") #so aceit numeros e o hifen so pode estar em uma posição 


class ConsultaRequest(BaseModel):
    cep: str

    @field_validator("cep")
    @classmethod
    def validar_cep(cls, valor: str) -> str:
        valor = valor.strip()
        if not CEP_REGEX.fullmatch(valor):
            raise ValueError("CEP deve estar no formato 12345678 ou 12345-678")
        return valor.replace("-", "")


#classe de regra de negocio responsavel por entregar uma requisição no formato correto
class ConsultaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # <-- ESSENCIAL PARA LER DO SQLALCHEMY!

    cep: str
    logradouro: str
    bairro: str
    cidade: str
    data_consulta: datetime = Field(serialization_alias="dataConsulta")


class HistoricoResponse(ConsultaResponse):
    id: int