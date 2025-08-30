import json
import os
from datetime import timedelta, date
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

load_dotenv()

CONFIG = {
    "WEEK_DAYS": {
        "SEGUNDA-FEIRA": 0, "TERÇA-FEIRA": 1, "QUARTA-FEIRA": 2,
        "QUINTA-FEIRA": 3, "SEXTA-FEIRA": 4,
    },
    "CAMPUS_MAPPING": {
        "SÃO CRISTÓVÃO": "sao-cristovao", "LAGARTO": "lagarto",
        "ITABAIANA": "itabaiana", "SERTÃO": "sertao",
        "HU/LARAN/DANÇA": "central"
    },
    "SUPPLIER_MAPPING": {
        "ISM RESTAURANTES LTDA": "ism-restaurantes-ltda",
        "PRS ALIMENTAÇÃO E SERVIÇOS LTDA": "prs-alimentacao-e-servicos-ltda",
    },
    "MEAL_TYPE_MAPPING": {
        "ALMOÇO": "lunch", "JANTAR": "dinner",
    },
    "CAMPUS_ENV_KEYS": {
        "sao-cristovao": "SHEET_ID_SAO_CRISTOVAO",
        "lagarto": "SHEET_ID_LAGARTO",
        "itabaiana": "SHEET_ID_ITABAIANA",
        "sertao": "SHEET_ID_SERTAO",
        "central": "SHEET_ID_CENTRAL",
    }
}


class MenuScraper:
    """
    Encapsula toda a lógica para buscar, processar e estruturar
    os dados do cardápio de uma planilha do Google Sheets.
    """

    def __init__(self, sheet_id: str):
        if not sheet_id:
            raise ValueError("O sheet_id não pode ser nulo.")
        self.sheet_id = sheet_id
        self.url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
        self.raw_data = self._fetch_sheet_data()
        self.monday_date = self._get_current_week_monday()

    def _fetch_sheet_data(self) -> List[Tuple[str, str]]:
        """Busca os dados da planilha e os retorna como uma lista de tuplas."""
        try:
            df = pd.read_csv(self.url, usecols=[1, 2], dtype=str).fillna('')
            return [tuple(row) for row in df.to_numpy()]
        except Exception as e:
            logging.error(f"Falha ao buscar ou processar a planilha {self.sheet_id}. Erro: {e}")
            return []

    @staticmethod
    def _get_current_week_monday() -> date:
        """Calcula a data da segunda-feira da semana atual."""
        today = date.today()
        return today - timedelta(days=today.weekday())

    @staticmethod
    def _clean_text(text: str) -> str:
        """Remove quebras de linha e espaços extras de um texto."""
        return ' '.join(text.replace('\n', ' ').replace('\r', ' ').split())

    def _group_meals_by_day(self) -> List[List[Tuple[str, str]]]:
        """Agrupa as linhas da planilha por dia da semana."""
        meals_by_day = []
        for left_cell, right_cell in self.raw_data:
            if right_cell in CONFIG["WEEK_DAYS"]:
                meals_by_day.append([])
            if meals_by_day:
                meals_by_day[-1].append((left_cell, right_cell))
        return meals_by_day

    def process_sheet(self) -> List[Dict[str, Any]]:
        """Orquestra o processo de extração e estruturação dos dados."""
        if not self.raw_data:
            return []
        try:
            campus_raw = self.raw_data[0][1]
            supplier_raw = self.raw_data[1][0]

            campus = CONFIG["CAMPUS_MAPPING"].get(campus_raw)
            supplier = CONFIG["SUPPLIER_MAPPING"].get(supplier_raw)

            if not campus or not supplier:
                logging.warning(
                    f"Campus '{campus_raw}' ou fornecedor '{supplier_raw}' não reconhecido na planilha {self.sheet_id}.")
                return []
        except IndexError:
            logging.error(
                f"Formato inesperado na planilha {self.sheet_id}. Não foi possível extrair campus/fornecedor.")
            return []

        grouped_meals = self._group_meals_by_day()
        structured_meals = []

        for meal_group in grouped_meals:
            header, _, *items_raw = meal_group
            meal_type_raw, week_day_raw = header

            meal_type = CONFIG["MEAL_TYPE_MAPPING"].get(meal_type_raw)
            week_day_index = CONFIG["WEEK_DAYS"].get(week_day_raw)

            if meal_type is None or week_day_index is None:
                logging.warning(f"Tipo de refeição ou dia da semana inválido encontrado: '{header}'")
                continue

            meal_date = self.monday_date + timedelta(days=week_day_index)

            items = [
                {
                    "item_type": self._clean_text(item_type),
                    "description": self._clean_text(description)
                }
                for item_type, description in items_raw
            ]

            meal_id = f"{campus}_{meal_date.strftime('%Y-%m-%d')}_{meal_type}"

            structured_meals.append({
                "id": meal_id,
                "campus": campus,
                "supplier": supplier,
                "meal_type": meal_type,
                "date": meal_date.strftime("%Y-%m-%d"),
                "items": items
            })

        return structured_meals


def main():
    """
    Função principal que itera sobre as planilhas definidas nas variáveis de ambiente,
    processa cada uma e imprime o resultado.
    """
    all_campus_meals = {}
    for campus_slug, env_key in CONFIG["CAMPUS_ENV_KEYS"].items():
        sheet_id = os.getenv(env_key)
        if not sheet_id:
            logging.warning(f"Variável de ambiente {env_key} não encontrada. Pulando o campus {campus_slug}.")
            continue

        logging.info(f"Processando cardápio para o campus: {campus_slug}")

        try:
            scraper = MenuScraper(sheet_id)
            meals = scraper.process_sheet()
            all_campus_meals[campus_slug] = meals
            logging.info(f"Encontradas {len(meals)} refeições para {campus_slug}.")
            print(json.dumps(meals, ensure_ascii=False, indent=2))
        except ValueError as e:
            logging.error(f"Erro ao instanciar o scraper para {env_key}: {e}")
        except Exception as e:
            logging.error(f"Ocorreu um erro inesperado ao processar {env_key}: {e}")


if __name__ == "__main__":
    main()