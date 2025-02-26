# tests/test_calculations.py
import sys
import os

# Ensure the project root is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_calculate():
    payload = {"value1": 3.5, "value2": 4.5}
    response = client.post("/calculations", json=payload)
    assert response.status_code == 200
    # Expected result is 3.5 + 4.5 = 8.0; also expect a uid in the response.
    data = response.json()
    assert "uid" in data
    assert data["result"] == 8.0

