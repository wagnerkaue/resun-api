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
        all_values = sheet.get_all_values()

        for row, col in self.posicao_alimentos:
            if row - 1 >= len(all_values) or col - 1 >= len(all_values[row - 1]):
                continue

            texto_na_posicao = all_values[row - 1][col - 1]

            if not texto_na_posicao or texto_na_posicao.strip() == "":
                continue

            texto_na_posicao = " ".join(texto_na_posicao.replace("\n", " ").replace("\r", " ").split())

            id_alimento = id_alimentos_mapa.get(texto_na_posicao)
            if id_alimento is None:
                raise RuntimeError(
                    f"Texto não mapeado em id_alimentos_mapa: '{texto_na_posicao}' na posição: linha={row}, coluna={col}")

            id_alimentos.append(id_alimento)

        return id_alimentos

    def extrair_data_baseado_na_semana_atual(self):
        hoje = datetime.now()
        dia_da_semana_hoje = hoje.weekday()
        dia_semana_cardapio = self.dia_semana.value
        segunda = hoje - timedelta(days=dia_da_semana_hoje)
        dia_do_cardapio = segunda + timedelta(days=dia_semana_cardapio)
        return dia_do_cardapio.strftime("%Y-%m-%d")


@dataclasses.dataclass
class CardapioSemanalPlanilha:
    campus: Campus
    id_planilha: str
    id_alimentos_mapa: dict[str, str]
    fornecedor: Fornecedor
    cardapios_diarios: list[CardapioDiarioPlanilha]

    def obter_sheet(self):
        client = get_gspread_client_service_account()
        spreadsheet = client.open_by_key(self.id_planilha)
        return spreadsheet.sheet1

    def extrair_cardapios(self):
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
                    self.id_alimentos_mapa
                )
            )
            cardapios.append(cardapio)
        return cardapios


sao_cristovao_planilha = CardapioSemanalPlanilha(
    campus=Campus.SAO_CRISTOVAO,
    id_planilha=os.getenv("SHEET_ID_SAO_CRISTOVAO"),
    id_alimentos_mapa={
        "ALFACE, CENOURA, PEPINO E MANGA": "salada_alface_cenoura_pepino_manga",
        "QUIABO E VAGEM À JARDINEIRA": "salada_quiabo_vagem_jardineira",
        "AZEITE E VINAGRE": "molho_azeite_vinagre",
        "LINHAÇA": "semente_linhaca",
        "BIFE AO MOLHO": "bife_ao_molho",
        "HAMBURGUÉR DE SOJA C/ MOLHO BARBECUE": "hamburguer_soja_molho_barbecue",
        "FEIJÃO CARIOCA TEMPERADO": "feijao_carioca",

        "FAROFA REFOGADA": "farofa_refogada",
        "ARROZ REFOGADO": "arroz_refogado",
        "FRUTA MELANCIA": "fruta_melancia",
        "SUCO DE CAJU": "suco_caju",

        "ISCAS DE FRANGO ACEBOLADO COM AZEITONAS": "iscas_frango_acebolado_azeitonas",
        "GRÃO DE BICO AO MOLHO POMODORO": "grao_de_bico_molho_pomodoro",
        "BATATA DOCE": "batata_doce",
        "CUSCUZ REFOGADO": "cuscuz",
        "SUCO DE MANGA": "suco_manga",
        "CAFÉ": "cafe",
        "FRUTA TANGERINA": "fruta_tangerina",

        "ACELGA, COUVE, CEBOLA ROXA E ABACAXI": "salada_acelga_couve_cebola_roxa_abacaxi",
        "CENOURA E ERVILHA REFOGADAS": "cenoura_ervilha_refogadas",
        "MOLHO DE ERVAS": "molho_de_ervas",
        "AMENDOIM": "semente_amendoim",
        "ESRTROGONOFE DE FRANGO": "strogonoff_de_frango",
        "GRÃO DE BICO AO MOLHO DE ERVAS": "grao_de_bico_molho_de_ervas",
        "BATATA DOCE ASSADA C/ ALECRIM": "batata_doce_assada_alecrim",
        "SUCO DE GOIABA": "suco_goiaba",

        "ISCA BOVINA À CHINESA": "isca_bovina_a_chinesa",
        "ALMONDEGA DE ERVILHA AO MOLHO MOSTARDA": "almondega_ervilha_molho_mostarda",
        "MACAXEIRA": "macaxeira",
        "CUSCUZ NORDESTINO": "cuscuz",
        "SUCO DE UMBU-CAJÁ": "suco_umbu_caja",
        "FRUTA GOIABA": "fruta_goiaba",

        "ALFACE, REPOLHO,TOMATE E AZEITONA": "salada_alface_repolho_tomate_azeitona",
        "ABÓBORA REFOGADA": "abobora_refogada",
        "MOLHO DE LARANJA": "molho_de_laranja",
        "CHIA": "semente_chia",
        "PICADINHO DE CARNE ACEBOLADA": "picadinho_carne_acebolada",
        "KIBE AO MOLHO DE ALHO": "kibe_molho_de_alho",
        "ABOBRINHA REFOGADA": "abobrinha_refogada",
        "FRUTA MELÃO": "fruta_melao",

        "FILÉ DE PEIXE À GOMES DE SÁ": "file_peixe_gomes_de_sa",
        "MOQUECA DE BANANA DA TERRA": "moqueca_banana_da_terra",
        "PURÊ DE BATATA": "pure_de_batata",
        "ARROZ COM COUVE": "arroz_com_couve",
        "SUCO DE UVA": "suco_uva",
        "FRUTA LARANJA": "fruta_laranja",

        "CENOURA, ACELGA, COUVE, TOMATE E MILHO": "salada_cenoura_acelga_couve_tomate_milho",
        "MIX DE REPOLHO REFOGADO": "mix_repolho_refogado",
        "MOLHO DE LIMÃO": "molho_de_limao",
        "SEMENTE DE ABÓBORA": "semente_de_abobora",
        "SOBRECOXA CAIPIRA": "sobrecoxa_caipira",
        "LENTILHA AO MOLHO DE TOMATE": "lentilha_molho_de_tomate",
        "MACARRÃO PARAFUSO AO ALHO E OLEO": "macarrao_parafuso_alho_e_oleo",
        "FRUTA BANANA": "fruta_banana",
        "SUCO DE UMBU": "suco_umbu",

        "CARNE DO SOL ACEBOLADA": "carne_de_sol_acebolada",
        "TORTA DE RICOTA E ESPINAFRE": "torta_ricota_espinafre",
        "BANANA DA TERRA": "banana_da_terra",
        "SUCO DE CAJÁ": "suco_caja",
        "FRUTA MAÇÃ": "fruta_maca",

        "VINAGRETE": "vinagrete",
        "BETERRABA COM VAGEM E MILHO REFOGADOS": "beterraba_vagem_milho_refogados",
        "BISTECA SUÍNA ASSADA": "bisteca_suina_assada",
        "ERVILHA AO MOLHO BRANCO": "ervilha_molho_branco",
        "PURÊ MISTO": "pure_misto",
        "SUCO DE MARACUJÁ": "suco_maracuja",

        "CUBOS DE FRANGO AO MOLHO POMODORO": "cubos_frango_molho_pomodoro",
        "LASANHA DE ABOBRINHA": "lasanha_de_abobrinha",
        "SELETA DE LEGUMES": "seleta_de_legumes",
        "MACARRÃO PARAFUSO REFOGADO COM ERVAS": "macarrao_parafuso_ervas"
    },
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
    id_alimentos_mapa = {
        "ACELGA E REPOLHO": "salada_acelga_repolho",
        "VINAGRETE": "vinagrete",
        "AZEITE, VINAGRE E SAL": "molho_azeite_vinagre",
        "AMENDOIM": "semente_amendoim",
        "ISCA DE FRANGO ACEBOLADA": "isca_frango_acebolada",
        "FALAFEL DE GRÃO DE BICO AO MOLHO DE TOMATE": "falafel_grao_de_bico_molho_tomate",
        "CENOURA, CHUCHU E VAGEM REFOGADOS": "cenoura_chuchu_vagem_refogados",
        "FEIJÃO CARIOCA": "feijao_carioca",
        "ARROZ PARBOILIZADO": "arroz_parboilizado",
        "BANANA": "fruta_banana",
        "SUCO DE GOIABA": "suco_goiaba",

        "PICADINHO MISTO": "picadinho_misto",
        "HAMBÚRGUER DE ERVILHA": "hamburguer_de_ervilha",
        "SOPA DE LEGUMES": "sopa_de_legumes",
        "CUSCUZ DE MILHO TEMPERADO": "cuscuz",
        "LARANJA": "fruta_laranja",
        "CAFÉ /LEITE": "cafe_leite",
        "CAFÉ": "cafe",
        "LEITE": "leite",
        "SUCO DE MARACUJÁ": "suco_maracuja",

        "ALFACE E CEBOLIMJA": "salada_alface_cebolinha",
        "CENOURA RALADA E MILHO VERDE": "salada_cenoura_ralada_milho_verde",
        "AZEITE, LIMÃO, ORÉGANO E SAL": "molho_limao",
        "XERÉM DE CASTANHA": "semente_xerem_castanha",
        "CUBOS DE CARNE BOVINA AO MOLHO MADEIRA": "cubos_carne_molho_madeira",
        "TORTA DE ERVILHA COM LEGUMES": "torta_ervilha_legumes",
        "PURÊ DE BATATA DOCE": "pure_batata_doce",
        "GOIABA": "fruta_goiaba",
        "SUCO DE ACEROLA": "suco_acerola",

        "FILÉ DE FRANGO EMPANADO": "file_frango_empanado",
        "LENTILHA COZIDA COM LEGUMES": "lentilha_cozida_legumes",
        "BANANA DA TERRA": "banana_da_terra",
        "CUSCUZ DE MILHO": "cuscuz",
        "ABACAXI": "fruta_abacaxi",
        "SUCO DE UMBU-CAJÁ": "suco_umbu_caja",

        "REPOLHO E COENTRO": "salada_repolho_coentro",
        "ACELGA E MANGA": "salada_acelga_manga",
        "AZEITE, VINAGRE BALSÂMICO E SAL": "molho_vinagre_balsamico",
        "GERGELIM": "semente_gergelim",
        "ESTROGONOFE DE FRANGO": "strogonoff_de_frango",
        "ESTROGONOFE DE SOJA": "strogonoff_de_soja",
        "ABÓBORA, BATATA INGLESA e CENOURA COZIDOS": "abobora_batata_cenoura_cozidos",
        "ARROZ PARBOILIZADO COM AÇAFRÃO": "arroz_parboilizado_acafrao",
        "TANGERINA": "fruta_tangerina",
        "SUCO DE ABACAXI": "suco_abacaxi",

        "CARNE MOÍDA": "carne_moida",
        "SOJA REFOGADA": "soja_refogada",
        "MACARRÃO AO MOLHO": "macarrao_ao_molho",
        "SELETA DE LEGUMES": "seleta_de_legumes",
        "MELANCIA": "fruta_melancia",
        "SUCO DE MANGA": "suco_manga",

        "COUVE EM TIRAS": "couve_em_tiras",
        "AZEITE, LIMÃO E SAL": "molho_limao",
        "LINHAÇA": "semente_linhaca",
        "CARNES DA FEIJOADA": "carnes_da_feijoada",
        "FEIJOADA VEGANA": "feijoada_vegana",
        "MACARRÃO AO MOLHO DE TOMATE": "macarrao_molho_tomate",
        "FEIJÃO PRETO": "feijao_preto",
        "SUCO DE MANGABA": "suco_mangaba",

        "PEITO DE FRANGO ENSOPADO": "peito_frango_ensopado",
        "ENSOPADO DE SOJA": "ensopado_de_soja",
        "INHAME": "inhame",
        "MAÇÃ": "fruta_maca",
        "SUCO DE CAJU": "suco_caju",

        "ALFACE E REPOLHO ROXO": "salada_alface_repolho_roxo",
        "BETERRABA RALADA": "beterraba_ralada",
        "AZEITE, VINAGRE, ORÉGANO E SAL": "molho_azeite_vinagre_oregano",
        "CHIA": "semente_chia",
        "FILÉ DE FRANGO AO MOLHO VERMELHO": "file_frango_molho_vermelho",
        "MOQUECA DE BANANA DA TERRA E GRÃO DE BICO": "moqueca_banana_terra_grao_de_bico",
        "BATATA E VAGEM SALTEADOS": "batata_vagem_salteados",
        "MOUSSE DE LIMÃO": "mousse_de_limao",

        "SOBRECOXA AO FORNO": "sobrecoxa_ao_forno",
        "ALMÔNDEGA DE LENTILHA": "almondega_de_lentilha",
        "CREME DE MACAXEIRA": "creme_de_macaxeira",
        "MELÃO": "fruta_melao",
        "SUCO DE CAJÁ": "suco_caja"
    },
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
    id_alimentos_mapa={
        "ALFACE, CENOURA, PEPINO E MANGA": "salada_alface_cenoura_pepino_manga",
        "QUIABO E VAGEM À JARDINEIRA": "salada_quiabo_vagem_jardineira",
        "AZEITE E VINAGRE": "molho_azeite_vinagre",
        "LINHAÇA": "semente_linhaca",
        "BIFE AO MOLHO": "bife_ao_molho",
        "HAMBURGUÉR DE SOJA C/ MOLHO BARBECUE": "hamburguer_soja_molho_barbecue",
        "FAROFA REFOGADA": "farofa_refogada",
        "ARROZ REFOGADO": "arroz_refogado",
        "FEIJÃO CARIOCA TEMPERADO": "feijao_carioca",
        "FRUTA MELANCIA": "fruta_melancia",
        "SUCO DE CAJU": "suco_caju",

        "ACELGA, COUVE, CEBOLA ROXA E ABACAXI": "salada_acelga_couve_cebola_roxa_abacaxi",
        "CENOURA E ERVILHA REFOGADAS": "cenoura_ervilha_refogadas",
        "MOLHO DE ERVAS": "molho_de_ervas",
        "AMENDOIM": "semente_amendoim",
        "ESRTROGONOFE DE FRANGO": "strogonoff_de_frango",
        "GRÃO DE BICO AO MOLHO DE ERVAS": "grao_de_bico_molho_de_ervas",
        "BATATA DOCE ASSADA C/ ALECRIM": "batata_doce_assada_alecrim",
        "FRUTA TANGERINA": "fruta_tangerina",
        "SUCO DE GOIABA": "suco_goiaba",

        "ALFACE, REPOLHO,TOMATE E AZEITONA": "salada_alface_repolho_tomate_azeitona",
        "ABÓBORA REFOGADA": "abobora_refogada",
        "MOLHO DE LARANJA": "molho_de_laranja",
        "CHIA": "semente_chia",
        "PICADINHO DE CARNE ACEBOLADA": "picadinho_carne_acebolada",
        "KIBE AO MOLHO DE ALHO": "kibe_molho_de_alho",
        "ABOBRINHA REFOGADA": "abobrinha_refogada",
        "FRUTA MELÃO": "fruta_melao",
        "SUCO DE MANGA": "suco_manga",

        "CENOURA, ACELGA, COUVE, TOMATE E MILHO": "salada_cenoura_acelga_couve_tomate_milho",
        "MIX DE REPOLHO REFOGADO": "mix_repolho_refogado",
        "MOLHO DE LIMÃO": "molho_de_limao",
        "SEMENTE DE ABÓBORA": "semente_de_abobora",
        "SOBRECOXA CAIPIRA": "sobrecoxa_caipira",
        "LENTILHA AO MOLHO DE TOMATE": "lentilha_molho_de_tomate",
        "MACARRÃO PARAFUSO AO ALHO E OLEO": "macarrao_parafuso_alho_e_oleo",
        "FRUTA BANANA": "fruta_banana",
        "SUCO DE UMBU": "suco_umbu",

        "VINAGRETE": "vinagrete",
        "BETERRABA COM VAGEM E MILHO REFOGADOS": "beterraba_vagem_milho_refogados",
        "BISTECA SUÍNA ASSADA": "bisteca_suina_assada",
        "ERVILHA AO MOLHO BRANCO": "ervilha_molho_branco",
        "PURÊ MISTO": "pure_misto",
        "FRUTA GOIABA": "fruta_goiaba",
        "SUCO DE MARACUJÁ": "suco_maracuja"
    },
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
    id_alimentos_mapa={
        "REPOLHO COM TOMATE": "salada_repolho_tomate",
        "BETERRABA RALADA COM UVAS PASSAS": "beterraba_ralada_uvas_passas",
        "AZEITE+ VINAGRE + ALHO FRITO": "molho_azeite_vinagre_alho",
        "LINHAÇA": "semente_linhaca",
        "ISCA DE FRANGO COM MOLHO AGRIDOCE": "isca_frango_molho_agridoce",
        "OMELETE\" DE GRÃO DE BICO E AVEIA": "omelete_grao_de_bico_aveia",
        "MACARRÃO AO MOLHO DE TOMATE": "macarrao_molho_tomate",
        "FEIJÃO CARIOCA E CALDO": "feijao_carioca",
        "ARROZ COM BRÓCOLIS": "arroz_com_brocolis",
        "ABACAXI": "fruta_abacaxi",
        "SUCO DE GOIABA": "suco_goiaba",

        "ALFACE E CENOURA": "salada_alface_cenoura",
        "TOMATE, PEPINO E CEBOLINHA": "salada_tomate_pepino_cebolinha",
        "AZEITE, VINAGRE E ÓREGANO": "molho_azeite_vinagre_oregano",
        "AMENDOIM TRITURADO": "semente_amendoim",
        "PICADINHO DE CARNE": "picadinho_de_carne",
        "HAMBÚRGUER DE LENTILHA": "hamburguer_de_lentilha",
        "BATATA INGLESA RÚSTICA": "batata_inglesa_rustica",
        "FEIJÃO PRETO": "feijao_preto",
        "ARROZ": "arroz",
        "MAÇÃ": "fruta_maca",
        "SUCO DE ACEROLA": "suco_acerola",

        "REPOLHO, RÚCULA E MANGA": "salada_repolho_rucula_manga",
        "TOMATE, CEBOLA ROXA E MANJERICÃO": "salada_tomate_cebola_roxa_manjericao",
        "AZEITE, MOSTARDA E MEL": "molho_mostarda_e_mel",
        "GERGELIM": "semente_gergelim",
        "SOBRECOXA COZIDA COM BATATA E CENOURA": "sobrecoxa_cozida_batata_cenoura",
        "FALAFEL AO MOLHO DE ALHO": "falafel_molho_de_alho",
        "FAROFA DE BANANA": "farofa_de_banana",
        "FEIJÃO CARIOCA": "feijao_carioca",
        "LARANJA": "fruta_laranja",
        "SUCO DE UMBU-CAJÁ": "suco_umbu_caja",

        "COUVE, CENOURA E ABACAXI": "salada_couve_cenoura_abacaxi",
        "ABOBRINHA COM HORTELÃ": "salada_abobrinha_hortela",
        "AZEITE E LIMÃO": "molho_limao",
        "XERÉM DE CASTANHA": "semente_xerem_castanha",
        "FILÉ DE PEIXE EMPANADO": "file_peixe_empanado",
        "JARDINEIRA DE SOJA": "jardineira_de_soja",
        "PURÊ RÚSTICO DE ABÓBORA": "pure_rustico_abobora",
        "TANGERINA": "fruta_tangerina",
        "SUCO DE MANGA": "suco_manga",

        "ALFACE, REPOLHO ROXO E LARANJA": "salada_alface_repolho_roxo_laranja",
        "ERVILHA E PEPINO": "salada_ervilha_pepino",
        "AZEITE E VINAGRE": "molho_azeite_vinagre",
        "CHIA": "semente_chia",
        "BISTECA SUÍNA ASSADA AO MOLHO BARBECUE": "bisteca_suina_assada_barbecue",
        "COGUMELO XADREZ": "cogumelo_xadrez",
        "CENOURA, CHUCHU E VAGEM REFOGADOS NO AZEITE, ALHO, CEBOLA E COENTRO": "cenoura_chuchu_vagem_refogados",
        "FEIJÃO TROPEIRO (FRADINHO)": "feijao_tropeiro_fradinho",
        "ARROZ COM AÇAFRÃO": "arroz_com_acafrao",
        "DOCE DE LEITE": "doce_de_leite",
        "SUCO DE CAJU": "suco_caju"
    },
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
    id_alimentos_mapa = {
        "ACELGA E REPOLHO": "salada_acelga_repolho",
        "VINAGRETE": "vinagrete",
        "AZEITE, VINAGRE E SAL": "molho_azeite_vinagre",
        "AMENDOIM": "semente_amendoim",
        "ISCA DE FRANGO ACEBOLADA": "isca_frango_acebolada",
        "FALAFEL DE GRÃO DE BICO AO MOLHO DE TOMATE": "falafel_grao_de_bico_molho_tomate",
        "CENOURA, CHUCHU E VAGEM REFOGADOS": "cenoura_chuchu_vagem_refogados",
        "FEIJÃO CARIOCA": "feijao_carioca",
        "ARROZ PARBOILIZADO": "arroz_parboilizado",
        "BANANA": "fruta_banana",
        "SUCO DE GOIABA": "suco_goiaba",

        "ALFACE E CEBOLIMJA": "salada_alface_cebolinha",
        "CENOURA RALADA E MILHO VERDE": "salada_cenoura_ralada_milho_verde",
        "AZEITE, LIMÃO, ORÉGANO E SAL": "molho_limao",
        "XERÉM DE CASTANHA": "semente_xerem_castanha",
        "CUBOS DE CARNE BOVINA AO MOLHO MADEIRA": "cubos_carne_molho_madeira",
        "TORTA DE ERVILHA COM LEGUMES": "torta_ervilha_legumes",
        "PURÊ DE BATATA DOCE": "pure_batata_doce",
        "GOIABA": "fruta_goiaba",
        "SUCO DE ACEROLA": "suco_acerola",

        "REPOLHO E COENTRO": "salada_repolho_coentro",
        "ACELGA E MANGA": "salada_acelga_manga",
        "AZEITE, VINAGRE BALSÂMICO E SAL": "molho_vinagre_balsamico",
        "GERGELIM": "semente_gergelim",
        "ESTROGONOFE DE FRANGO": "strogonoff_de_frango",
        "ESTROGONOFE DE SOJA": "strogonoff_de_soja",
        "ABÓBORA, BATATA INGLESA e CENOURA COZIDOS": "abobora_batata_cenoura_cozidos",
        "ARROZ PARBOILIZADO COM AÇAFRÃO": "arroz_parboilizado_acafrao",
        "TANGERINA": "fruta_tangerina",
        "SUCO DE ABACAXI": "suco_abacaxi",

        "COUVE EM TIRAS": "couve_em_tiras",
        "AZEITE, LIMÃO E SAL": "molho_limao",
        "LINHAÇA": "semente_linhaca",
        "CARNES DA FEIJOADA": "carnes_da_feijoada",
        "FEIJOADA VEGANA": "feijoada_vegana",
        "MACARRÃO AO MOLHO DE TOMATE": "macarrao_molho_tomate",
        "FEIJÃO PRETO": "feijao_preto",
        "LARANJA": "fruta_laranja",
        "SUCO DE MANGABA": "suco_mangaba",

        "ALFACE E REPOLHO ROXO": "salada_alface_repolho_roxo",
        "BETERRABA RALADA": "beterraba_ralada",
        "AZEITE, VINAGRE, ORÉGANO E SAL": "molho_azeite_vinagre_oregano",
        "CHIA": "semente_chia",
        "FILÉ DE FRANGO AO MOLHO VERMELHO": "file_frango_molho_vermelho",
        "MOQUECA DE BANANA DA TERRA E GRÃO DE BICO": "moqueca_banana_terra_grao_de_bico",
        "BATATA E VAGEM SALTEADOS": "batata_vagem_salteados",
        "MOUSSE DE LIMÃO": "mousse_de_limao",
        "SUCO DE MARACUJÁ": "suco_maracuja"
    },
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

def obter_todos_cardapios_dessa_semana():
    cardapios = []
    for cardapio_semanal in TODOS_CARDAPIOS_SEMANAIS_PLANILHAS:
        cardapios.extend(cardapio_semanal.extrair_cardapios())
    return cardapios


if __name__ == "__main__":
    from tabulate import tabulate
    cardapios = obter_todos_cardapios_dessa_semana()
    tabela = [
        [c.data, c.campus, c.tipo_refeicao, ", ".join(c.id_alimentos)]
        for c in cardapios
    ]
    print(tabulate(tabela, headers=["Data", "Campus", "Refeição", "Itens"]))
