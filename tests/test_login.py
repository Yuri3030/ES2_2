import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

# Testa a rota personalizada /login com JSON
@pytest.mark.asyncio
async def test_login_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/login", json={
            "email": "lucas@example.com",
            "password": "lucas"
        })
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert data["message"] == "Login realizado com sucesso!"

# Testa a rota padrão OAuth2 /token com form-urlencoded
@pytest.mark.asyncio
async def test_oauth2_login_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/token", data={
            "username": "lucas@example.com",
            "password": "lucas"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
