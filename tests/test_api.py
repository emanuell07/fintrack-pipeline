import pytest
from fastapi.testclient import TestClient
from api.main import app
import os
from dotenv import load_dotenv

load_dotenv(encoding='latin-1')
API_KEY = os.getenv("API_KEY")

client = TestClient(app)
headers = {"X-API-Key": API_KEY}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FinTrack API rodando!"}

def test_get_all_summaries():
    response = client.get("/summary/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_summary_sem_auth():
    response = client.get("/summary/")
    assert response.status_code == 403

def test_get_summary_by_usuario():
    response = client.get("/summary/usuario/1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert all(item['usuario_id'] == 1 for item in data)

def test_get_summary_by_mes():
    response = client.get("/summary/mes/2026/1", headers=headers)
    assert response.status_code == 200

def test_get_summary_usuario_inexistente():
    response = client.get("/summary/usuario/9999", headers=headers)
    assert response.status_code == 200
    assert response.json() == []