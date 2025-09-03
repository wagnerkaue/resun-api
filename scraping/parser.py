import dataclasses
from datetime import date, timedelta

from modelos import Bandejao, Campus, Fornecedor, TipoRefeicao, Cardapio
from scraping.mapeamentos_base import MapeamentoCardapio, MapeamentoBandejao


class ParserBase:
    def __init__(self, dados: list[list[str]]):
        self.dados = dados

    def texto_na_posicao(self, posicao: tuple[int, int]) -> str:
        try:
            return self.dados[posicao[0] - 1][posicao[1] - 1]
        except IndexError:
            return ""

    @staticmethod
    def limpar_texto_celula(texto: str) -> str:
        """
        Limpa o texto de uma única célula: normaliza quebras de linha,
        remove espaços extras e converte para minúsculas.
        """
        if not texto:
            return ""

        palavras = texto.split()
        return " ".join(palavras).lower()


class ParserBandejao(ParserBase):
    def __init__(self, mapa_bandejao: MapeamentoBandejao, dados: list[list[str]]):
        self.mapa_bandejao = mapa_bandejao
        super().__init__(dados)

    def extrair(self) -> Bandejao:
        dados_extraidos = {}
        for field in dataclasses.fields(self.mapa_bandejao):
            posicoes = getattr(self.mapa_bandejao, field.name)
            itens_finais = [
                self.limpar_texto_celula(self.texto_na_posicao(pos))
                for pos in posicoes
                if self.limpar_texto_celula(self.texto_na_posicao(pos))
            ]
            dados_extraidos[field.name] = itens_finais
        return Bandejao(**dados_extraidos)


class ParserCardapio(ParserBase):
    _CAMPUS_MAP = {
        "SÃO CRISTÓVÃO": Campus.SAO_CRISTOVAO,
        "ITABAIANA": Campus.ITABAIANA,
        "HU/LARAN/DANÇA": Campus.CENTRAL,
        "LAGARTO": Campus.LAGARTO,
        "SERTÃO": Campus.SERTAO
    }
    _FORNECEDOR_MAP = {
        "ISM RESTAURANTES LTDA": Fornecedor.ISM,
        "PRS ALIMENTAÇÃO E SERVIÇOS LTDA": Fornecedor.PRS
    }
    _REFEICAO_MAP = {
        "ALMOÇO": TipoRefeicao.ALMOCO,
        "JANTAR": TipoRefeicao.JANTAR
    }
    _DIA_SEMANA_MAP = {
        "SEGUNDA-FEIRA": 0, "TERÇA-FEIRA": 1, "QUARTA-FEIRA": 2,
        "QUINTA-FEIRA": 3, "SEXTA-FEIRA": 4
    }

    def __init__(self, mapa_cardapio: MapeamentoCardapio, dados: list[list[str]]):
        self.mapa_cardapio = mapa_cardapio
        super().__init__(dados)

    def _mapear_texto_para_enum(self, posicao: tuple[int, int], mapa: dict, nome_campo: str):
        texto_bruto = self.texto_na_posicao(posicao)

        valor_enum = mapa.get(texto_bruto)
        if valor_enum is None:
            raise ValueError(f"'{nome_campo}' inesperado ou com formatação inválida: '{texto_bruto}'")
        return valor_enum

    def extrair_campus(self) -> Campus:
        return self._mapear_texto_para_enum(self.mapa_cardapio.campus, self._CAMPUS_MAP, "Campus")

    def extrair_fornecedor(self) -> Fornecedor:
        return self._mapear_texto_para_enum(self.mapa_cardapio.fornecedor, self._FORNECEDOR_MAP, "Fornecedor")

    def extrair_refeicao(self) -> TipoRefeicao:
        return self._mapear_texto_para_enum(self.mapa_cardapio.tipo_refeicao, self._REFEICAO_MAP, "Refeição")

    @staticmethod
    def _segunda_feira_dessa_semana() -> date:
        hoje = date.today()
        return hoje - timedelta(days=hoje.weekday())

    def extrair_data(self) -> date:
        texto_bruto = self.texto_na_posicao(self.mapa_cardapio.dia_da_semana)
        offset = self._DIA_SEMANA_MAP.get(texto_bruto)
        if offset is None:
            raise ValueError(f"Dia da semana inesperado ou com formatação inválida: '{texto_bruto}'")
        return self._segunda_feira_dessa_semana() + timedelta(days=offset)

    def extrair(self) -> Cardapio:
        parser_bandejao = ParserBandejao(self.mapa_cardapio.bandejao, self.dados)
        return Cardapio(
            campus=self.extrair_campus(),
            fornecedor=self.extrair_fornecedor(),
            data=self.extrair_data(),
            tipo_refeicao=self.extrair_refeicao(),
            bandejao=parser_bandejao.extrair(),
        )
