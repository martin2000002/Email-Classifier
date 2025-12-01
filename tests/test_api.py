import os
import pytest
import httpx

BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")


def test_root_status():
    r = httpx.get(f"{BASE_URL}/", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert "message" in data
    assert "model_status" in data


def test_classify_invalid():
    r = httpx.post(f"{BASE_URL}/classify", json={"email": ""}, timeout=5)
    assert r.status_code == 400


def test_classify_valid_when_model_present():
    root = httpx.get(f"{BASE_URL}/", timeout=5)
    assert root.status_code == 200
    if root.json().get("model_status") != "loaded":
        pytest.skip("Model not loaded on server; skipping valid classify test.")
    email = "Hi team, please process the attached invoice by Friday. Thanks."
    r = httpx.post(f"{BASE_URL}/classify", json={"email": email}, timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert "predicted_class" in data
    assert "probabilities" in data
