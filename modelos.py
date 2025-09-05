"""Modelos para a API do RESUN-UFS"""
from datetime import date
from enum import Enum
from typing import Optional

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

class Alimento(BaseModel):
    id: str = Field(description="ID único do alimento (slug)")
    nome: str = Field(description="Nome do alimento")
    categoria_id: str = Field(description="ID da categoria do alimento")
    categoria_nome: str = Field(description="Nome da categoria do alimento")
    imagem_url: Optional[str] = Field(default=None, description="URL da imagem do alimento")

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

class CardapioCompleto(Cardapio):
    """Modelo de resposta que inclui os objetos completos de Alimento."""
    id_alimentos: list[Alimento] = Field(description="Lista de objetos de alimentos servidos")

    # Renomeando o campo para clareza na resposta da API
    class Config:
        fields = {
            'id_alimentos': 'alimentos'
        }