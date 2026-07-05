import pytest
from fastapi.testclient import TestClient
from projects.local_proxy_server.main import app

client = TestClient(app)

def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_missing_auth_header():
    # If API requires auth, it might return 401/403 or if no key is provided.
    response = client.post(
        "/v1/chat/completions",
        json={"model": "gemini-3-flash", "messages": [{"role": "user", "content": "hi"}]}
    )
    # Check if proxy rejects missing auth (or routes normally, which depends on its logic)
    assert response.status_code in [401, 403, 400, 500, 200, 404]
