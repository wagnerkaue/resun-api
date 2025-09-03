import json
import os

from dotenv import load_dotenv
from modelos import Campus
from auth import get_sheets_service
from mapeamentos import MAPEAMENTO_BANDEJOES
from scraping.parser import ParserCardapio

load_dotenv()

ID_PLANILHAS = {
    Campus.SAO_CRISTOVAO: os.getenv("SHEET_ID_SAO_CRISTOVAO"),
    Campus.ITABAIANA: os.getenv("SHEET_ID_ITABAIANA"),
    Campus.LAGARTO: os.getenv("SHEET_ID_LAGARTO"),
    Campus.CENTRAL: os.getenv("SHEET_ID_CENTRAL"),
    Campus.SERTAO: os.getenv("SHEET_ID_SERTAO"),
}

NOME_ABAS = {
    Campus.SAO_CRISTOVAO: "CENTRAL",
    Campus.ITABAIANA: "ITABAIANA",
    Campus.LAGARTO: "LAGARTO",
    Campus.CENTRAL: "CENTRAL",
    Campus.SERTAO: "SERTAO"
}


def extrair_cardapios_api():
    cardapios = []

    sheets_service = get_sheets_service()

    for campus in Campus:
        id_planilha = ID_PLANILHAS.get(campus)
        nome_aba = NOME_ABAS.get(campus)
        print(f"Extraindo dados para o campus: {campus.value} (Aba: '{nome_aba}')...")

        try:
            result = sheets_service.spreadsheets().values().get(
                spreadsheetId=id_planilha,
                range=nome_aba
            ).execute()
            celulas = result.get('values', [])

            for mapeamento in MAPEAMENTO_BANDEJOES[campus]:
                parser = ParserCardapio(mapeamento, celulas)
                cardapio = parser.extrair()
                cardapios.append(cardapio)

        except Exception as e:
            print(f"  -> FALHA AO PROCESSAR CAMPUS '{campus.value}': {e}")

    return cardapios


def main():
    """
    Função principal para executar e testar a extração dos cardápios via API.
    """
    print("=" * 50)
    print("INICIANDO TESTE DE EXTRAÇÃO DE CARDÁPIOS (VIA API)")
    print("=" * 50)

    try:
        bandejoes_extraidos = extrair_cardapios_api()

        if not bandejoes_extraidos:
            print("\nNenhum cardápio foi extraído.")
            return

        print(f"\nEXTRAÇÃO CONCLUÍDA! Total de {len(bandejoes_extraidos)} cardápios encontrados.\n")

        for i, bandejao in enumerate(bandejoes_extraidos, 1):
            print(f"--- Cardápio {i}: {bandejao.id} ---")
            bandejao_dict = bandejao.model_dump(mode='json')
            pretty_json = json.dumps(bandejao_dict, indent=4, ensure_ascii=False)
            print(pretty_json)
            print("-" * 40 + "\n")

    except Exception as e:
        print(f"\nERRO CRÍTICO DURANTE A EXECUÇÃO: {e}")


if __name__ == "__main__":
    main()
