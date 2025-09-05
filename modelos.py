"""Modelos para a API do RESUN-UFS"""
from datetime import date
from enum import Enum

from pydantic import BaseModel, computed_field, Field, field_serializer


class Campus(str, Enum):
    SAO_CRISTOVAO = "sao-cristovao"
    LAGARTO = "lagarto"
    ITABAIANA = "itabaiana"
    SERTAO = "sertao"
    CENTRAL = "central"


class Fornecedor(str, Enum):
    ISM = "ism"
    PRS = "prs"


class TipoRefeicao(str, Enum):
    ALMOCO = "almoco"
    JANTAR = "jantar"


class Cardapio(BaseModel):
    campus: Campus = Field(description="Campus da UFS onde está o restaurante")
    fornecedor: Fornecedor = Field(description="Empresa fornecedora da refeição")
    tipo_refeicao: TipoRefeicao = Field(description="Tipo de refeição (almoço ou jantar)")
    data: date = Field(description="Data da refeição")
    id_alimentos: list[str]

    @field_serializer('data')
    def serialize_data(self, data: date, _info):
        """Serializa o objeto de data para uma string no formato AAAA-MM-DD."""
        return data.isoformat()

    @computed_field
    @property
    def id(self) -> str:
        """Identificador único do bandejão (campus + data + tipo_refeição)"""
        data_formatada = self.data.strftime("%Y-%m-%d")
        return f"{self.campus.value}_{data_formatada}_{self.tipo_refeicao.value}"
