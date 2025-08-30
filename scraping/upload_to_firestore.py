import os
import logging
from google.cloud import firestore
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPICallError

from scrape import MenuScraper, CONFIG

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def initialize_firestore(key_path: str):
    if not os.path.exists(key_path):
        logging.critical(f"O arquivo de chave de serviço não foi encontrado em: '{key_path}'")
        logging.critical("Faça o download da chave do seu projeto no Google Cloud e coloque-a no diretório do projeto.")
        return None

    try:
        credentials = service_account.Credentials.from_service_account_file(key_path)
        db = firestore.Client(credentials=credentials)

        logging.info("Cliente do Firestore inicializado com sucesso usando o arquivo de chave.")
        return db
    except Exception as e:
        logging.error(
            f"Não foi possível conectar ao Firestore usando '{key_path}'. Verifique o arquivo e suas permissões. Erro: {e}")
        return None


def upload_meals(db: firestore.Client, meals: list):
    """
    Faz o upload de uma lista de refeições para a coleção 'meals' no Firestore.
    (Esta função permanece exatamente a mesma)
    """
    if not meals:
        logging.info("Nenhuma refeição para fazer upload.")
        return

    meals_collection = db.collection("meals")
    logging.info(f"Iniciando o upload de {len(meals)} refeições para a coleção 'meals'...")

    for meal in meals:
        try:
            doc_id = meal["id"]
            meals_collection.document(doc_id).set(meal)
            logging.info(f"Documento '{doc_id}' salvo com sucesso.")
        except GoogleAPICallError as e:
            logging.error(f"Erro de API ao salvar o documento '{meal.get('id', 'ID_N/A')}': {e}")
        except KeyError:
            logging.error(f"Refeição mal formatada encontrada, sem chave 'id': {meal}")

    logging.info("Upload concluído.")


def main():
    KEY_FILE_PATH = "../serviceAccountKey.json"

    db = initialize_firestore(key_path=KEY_FILE_PATH)
    if not db:
        return

    all_meals = []

    for campus_slug, env_key in CONFIG["CAMPUS_ENV_KEYS"].items():
        sheet_id = os.getenv(env_key)
        if not sheet_id:
            logging.warning(f"Variável de ambiente {env_key} não encontrada. Pulando.")
            continue

        logging.info(f"Buscando dados para o campus: {campus_slug}")
        try:
            scraper = MenuScraper(sheet_id)
            meals = scraper.process_sheet()
            if meals:
                all_meals.extend(meals)
                logging.info(f"Encontradas {len(meals)} refeições para {campus_slug}.")
            else:
                logging.warning(f"Nenhuma refeição encontrada para {campus_slug}.")
        except Exception as e:
            logging.error(f"Falha ao processar a planilha para {campus_slug}. Erro: {e}")

    if all_meals:
        upload_meals(db, all_meals)
    else:
        logging.warning("Nenhuma refeição foi encontrada em nenhum dos campi para upload.")


if __name__ == "__main__":
    main()