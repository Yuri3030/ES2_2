import pytest
from httpx import AsyncClient

BASE_URL = "http://web:8000"

@pytest.mark.asyncio
async def test_admin_can_list_users():
    # Login como admin
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/login", json={
            "email": "admin@example.com",
            "password": "admin"
        })
    assert response.status_code == 200
    token = response.json()["token"]

    # Tenta listar usuários
    async with AsyncClient(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {token}"}
    ) as ac:
        response = await ac.get("/users/")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)



# Teste para listar usuários com usuário normal
# Este teste deve falhar, pois usuários normais não podem listar usuários
@pytest.mark.asyncio
async def test_normal_user_cannot_list_users():
    email = "normal@example.com"
    password = "123456"

    # Tenta criar o usuário, ignora se já existir
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/users/", json={
            "name": "Usuário Normal",
            "email": email,
            "password": password
        })
        if response.status_code not in [200, 400]:
            # 400 = já cadastrado, 200 = sucesso
            raise AssertionError("Falha ao criar usuário de teste")

    # Login com usuário comum
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/login", json={
            "email": email,
            "password": password
        })
    assert response.status_code == 200
    token = response.json()["token"]

    # Tenta listar usuários
    async with AsyncClient(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {token}"}
    ) as ac:
        response = await ac.get("/users/")
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Acesso restrito ao administrador."

