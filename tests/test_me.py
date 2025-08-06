import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_current_user():
    # Login com credenciais válidas
    login_data = {
        "username": "lucas@example.com",
        "password": "lucas"
    }

    async with AsyncClient(base_url="http://web:8000") as ac:
        login_response = await ac.post("/token", data=login_data)
        assert login_response.status_code == 200

        token = login_response.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Faz a requisição para o endpoint protegido /me
        response = await ac.get("/me", headers=headers)
        assert response.status_code == 200

        data = response.json()
        assert data["email"] == "lucas@example.com"
        assert "id" in data
        assert "name" in data
