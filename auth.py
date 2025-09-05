import os

import firebase_admin
import gspread
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

load_dotenv()


def _get_credentials():
    key_filename = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not key_filename:
        raise ValueError("Variável 'GOOGLE_APPLICATION_CREDENTIALS' não definida no .env")

    project_root = os.path.dirname(os.path.abspath(__file__))
    abs_key_path = os.path.join(project_root, key_filename)

    if not os.path.exists(abs_key_path):
        raise FileNotFoundError(f"Arquivo de credenciais não encontrado em '{abs_key_path}'")

    return abs_key_path


def get_gspread_client_service_account():
    """
    Retorna um gspread.Client usando gspread.service_account.
    Requer o JSON da conta de serviço local (caminho obtido por _get_credentials()).
    """
    abs_key_path = _get_credentials()
    # gspread.service_account já cria credentials internamente
    return gspread.service_account(filename=abs_key_path)


def get_firestore_client():
    try:
        firebase_admin.get_app()
    except ValueError:
        abs_key_path = _get_credentials()
        cred = credentials.Certificate(abs_key_path)
        firebase_admin.initialize_app(cred)
        print("Firebase inicializado com sucesso.")

    return firestore.client()
