import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from google.oauth2 import service_account
from googleapiclient.discovery import build

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


def get_sheets_service():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    abs_key_path = _get_credentials()

    creds = service_account.Credentials.from_service_account_file(abs_key_path, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service


def get_firestore_client():
    try:
        firebase_admin.get_app()
    except ValueError:
        abs_key_path = _get_credentials()
        cred = credentials.Certificate(abs_key_path)
        firebase_admin.initialize_app(cred)
        print("Firebase inicializado com sucesso.")

    return firestore.client()