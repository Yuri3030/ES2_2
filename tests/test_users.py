import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_list_users():
    # 1. Faz login com usuário válido
    login_data = {
        "username": "lucas@example.com",
        "password": "lucas"
    }

    async with AsyncClient(base_url="http://web:8000") as ac:
        login_response = await ac.post("/token", data=login_data)

        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # 2. Usa o token no header para acessar rota protegida
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = await ac.get("/users/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)