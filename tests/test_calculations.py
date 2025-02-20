# Tests for the calculation endpoint

import sys
import os

# Ensure the project root is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_calculate_sample():
    payload = {"value1": 3.5, "value2": 4.5}
    response = client.post("/calculations/sample", json=payload)
    assert response.status_code == 200
    # Expected result is 3.5 + 4.5 = 8.0
    assert response.json() == {"result": 8.0}
