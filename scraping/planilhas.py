import dataclasses
import os
from datetime import datetime, timedelta
from enum import IntEnum

from gspread import Worksheet

from auth import get_gspread_client_service_account
from modelos import Campus, Fornecedor, TipoRefeicao, Cardapio


class DiaSemana(IntEnum):
    SEGUNDA = 0
    TERCA = 1
    QUARTA = 2
    QUINTA = 3
    SEXTA = 4


@dataclasses.dataclass
class CardapioDiarioPlanilha:
    dia_semana: DiaSemana
    tipo_refeicao: TipoRefeicao
    posicao_alimentos: list[tuple[int, int]]

    def extrair_id_alimentos(self, sheet: Worksheet, id_alimentos_mapa: dict[str, str]):
        id_alimentos = []
        for posicao in self.posicao_alimentos:
            texto_na_posicao = sheet.cell(*posicao).value
            texto_na_posicao = " ".join(texto_na_posicao
                                        .replace("\n", " ")
                                        .replace("\r", " ")
                                        .split())
            id_alimento = id_alimentos_mapa.get(texto_na_posicao)
            if id_alimento is None:
                raise RuntimeError(f"Texto não esperado por alimentos_mapa: '{texto_na_posicao}'")
            id_alimentos.append(id_alimento)
        return id_alimentos

    def extrair_data_baseado_na_semana_atual(self):
        hoje = datetime.now()
        dia_da_semana_hoje = hoje.weekday()
        dia_semana_cardapio = self.dia_semana.value
        segunda = hoje - timedelta(days=dia_da_semana_hoje)
        dia_do_cardapio = segunda + timedelta(days=dia_semana_cardapio)
        return dia_do_cardapio


@dataclasses.dataclass
class CardapioSemanalPlanilha:
    campus: Campus
    id_planilha: str
    fornecedor: Fornecedor
    cardapios_diarios: list[CardapioDiarioPlanilha]

    def obter_sheet(self):
        client = get_gspread_client_service_account()
        spreadsheet = client.open_by_key(self.id_planilha)
        return spreadsheet.sheet1

    def extrair_cardapios(self, id_alimentos_mapa: dict[str, str]):
        sheet = self.obter_sheet()
        cardapios = []
        for cardapio_diario in self.cardapios_diarios:
            cardapio = Cardapio(
                campus=self.campus,
                fornecedor=self.fornecedor,
                tipo_refeicao=cardapio_diario.tipo_refeicao,
                data=cardapio_diario.extrair_data_baseado_na_semana_atual(),
                id_alimentos=cardapio_diario.extrair_id_alimentos(
                    sheet,
                    id_alimentos_mapa
                )
            )
            cardapios.append(cardapio)
        return cardapios


sao_cristovao_planilha = CardapioSemanalPlanilha(
    campus=Campus.SAO_CRISTOVAO,
    id_planilha=os.getenv("SHEET_ID_SAO_CRISTOVAO"),
    fornecedor=Fornecedor.ISM,
    cardapios_diarios=[
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEGUNDA,
            tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(6, 17)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEGUNDA,
            tipo_refeicao=TipoRefeicao.JANTAR,
            posicao_alimentos=[(r, 3) for r in range(19, 26)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.TERCA,
            tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(28, 39)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.TERCA,
            tipo_refeicao=TipoRefeicao.JANTAR,
            posicao_alimentos=[(r, 3) for r in range(41, 48)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUARTA,
            tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(50, 61)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUARTA,
            tipo_refeicao=TipoRefeicao.JANTAR,
            posicao_alimentos=[(r, 3) for r in range(63, 70)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUINTA,
            tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(72, 83)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUINTA,
            tipo_refeicao=TipoRefeicao.JANTAR,
            posicao_alimentos=[(r, 3) for r in range(85, 92)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEXTA,
            tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(94, 105)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEXTA,
            tipo_refeicao=TipoRefeicao.JANTAR,
            posicao_alimentos=[(r, 3) for r in range(107, 114)]
        ),
    ]
)

itabaiana_planilha = CardapioSemanalPlanilha(
    campus=Campus.ITABAIANA,
    id_planilha=os.getenv("SHEET_ID_ITABAIANA"),
    fornecedor=Fornecedor.PRS,
    cardapios_diarios=[
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEGUNDA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(7, 18)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEGUNDA, tipo_refeicao=TipoRefeicao.JANTAR,
            posicao_alimentos=[(r, 3) for r in range(20, 27)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.TERCA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(29, 40)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.TERCA, tipo_refeicao=TipoRefeicao.JANTAR,
            posicao_alimentos=[(r, 3) for r in range(42, 49)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUARTA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(51, 62)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUARTA, tipo_refeicao=TipoRefeicao.JANTAR,
            posicao_alimentos=[(r, 3) for r in range(64, 71)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUINTA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(73, 84)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUINTA, tipo_refeicao=TipoRefeicao.JANTAR,
            posicao_alimentos=[(r, 3) for r in range(86, 93)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEXTA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(95, 106)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEXTA, tipo_refeicao=TipoRefeicao.JANTAR,
            posicao_alimentos=[(r, 3) for r in range(108, 115)]
        ),
    ]
)

central_planilha = CardapioSemanalPlanilha(
    campus=Campus.CENTRAL,
    id_planilha=os.getenv("SHEET_ID_CENTRAL"),
    fornecedor=Fornecedor.ISM,
    cardapios_diarios=[
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEGUNDA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(6, 17)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.TERCA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(19, 30)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUARTA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(32, 43)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUINTA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(45, 56)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEXTA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(58, 69)]
        ),
    ]
)

lagarto_planilha = CardapioSemanalPlanilha(
    campus=Campus.LAGARTO,
    id_planilha=os.getenv("SHEET_ID_LAGARTO"),
    fornecedor=Fornecedor.PRS,
    cardapios_diarios=[
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEGUNDA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(6, 17)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.TERCA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(19, 30)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUARTA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(32, 43)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUINTA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(45, 56)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEXTA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(58, 69)]
        ),
    ]
)

sertao_planilha = CardapioSemanalPlanilha(
    campus=Campus.SERTAO,
    id_planilha=os.getenv("SHEET_ID_SERTAO"),
    fornecedor=Fornecedor.PRS,
    cardapios_diarios=[
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEGUNDA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(7, 18)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.TERCA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(20, 31)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUARTA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(33, 44)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.QUINTA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(46, 57)]
        ),
        CardapioDiarioPlanilha(
            dia_semana=DiaSemana.SEXTA, tipo_refeicao=TipoRefeicao.ALMOCO,
            posicao_alimentos=[(r, 3) for r in range(59, 70)]
        )
    ]
)

TODOS_CARDAPIOS_SEMANAIS_PLANILHAS = [
    sao_cristovao_planilha,
    itabaiana_planilha,
    central_planilha,
    lagarto_planilha,
    sertao_planilha
]

ALIMENTOS = {
    "FEIJÃO CARIOCA TEMPERADO": "feijao_carioca"
}


def obter_todos_cardapios_dessa_semana():
    cardapios = []
    for cardapio_semanal in TODOS_CARDAPIOS_SEMANAIS_PLANILHAS:
        cardapios.extend(cardapio_semanal.extrair_cardapios(ALIMENTOS))
    return cardapios


if __name__ == "__main__":
    cardapios = obter_todos_cardapios_dessa_semana()
