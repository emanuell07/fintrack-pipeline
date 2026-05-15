import requests
import os
from dotenv import load_dotenv

load_dotenv(encoding='latin-1')

BASE_URL = "http://127.0.0.1:8000"
API_KEY = os.getenv("API_KEY")
HEADERS = {"X-API-Key": API_KEY}

def get_all_summaries():
    response = requests.get(f"{BASE_URL}/summary/", headers=HEADERS)
    return response.json()

def get_summary_by_usuario(usuario_id: int):
    response = requests.get(f"{BASE_URL}/summary/usuario/{usuario_id}", headers=HEADERS)
    return response.json()

def get_summary_by_mes(ano: int, mes: int):
    response = requests.get(f"{BASE_URL}/summary/mes/{ano}/{mes}", headers=HEADERS)
    return response.json()