"""import pytest
from httpx import AsyncClient

BASE_URL = "http://web:8000"

@pytest.mark.asyncio
async def test_create_and_delete_user():
    temp_email = "tempuser@example.com"
    temp_password = "123456"
    common_email = "comum@example.com"
    common_password = "123456"
    admin_email = "admin@example.com"
    admin_password = "admin"

    # 0. Login como admin para garantir limpeza inicial (delete tempuser se existir)
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/login", json={
            "email": admin_email,
            "password": admin_password
        })
        assert response.status_code == 200
        admin_token = response.json()["token"]

        # Deleta tempuser se ele existir
        await ac.delete(
            f"/users/{temp_email}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

    # 1. Cria o usuário temporário
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/users/", json={
            "name": "Usuário Temporário",
            "email": temp_email,
            "password": temp_password
        })
        assert response.status_code == 200

    # 1.1 Login do usuário temporário para verificar que existe
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/login", json={
            "email": temp_email,
            "password": temp_password
        })
        assert response.status_code == 200
        print("Usuário temporário criado e autenticado com sucesso")

    # 2. Cria o usuário comum (caso ainda não exista)
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/users/", json={
            "name": "Usuário Comum",
            "email": common_email,
            "password": common_password
        })
        if response.status_code == 400:
            print("Usuário comum já existe, seguindo com o teste...")
        else:
            assert response.status_code == 200

    # 3. Login como usuário comum
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/login", json={
            "email": common_email,
            "password": common_password
        })
        assert response.status_code == 200
        common_token = response.json()["token"]

    # 4. Tentativa de deletar com usuário comum (não deve funcionar)
    async with AsyncClient(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {common_token}"}
    ) as ac:
        response = await ac.delete(f"/users/{temp_email}")
        print("Tentativa de deletar com usuário comum retornou:", response.status_code, response.text)
        assert response.status_code == 403

    # 5. Login como admin (já feito no início, reutiliza o token)

    # 6. Deleta o usuário com token do admin (deve funcionar)
    async with AsyncClient(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {admin_token}"}
    ) as ac:
        response = await ac.delete(f"/users/{temp_email}")
        assert response.status_code == 200
        assert "deletado" in response.json()["message"].lower()
        print("Usuário temporário deletado com sucesso pelo admin.")

"""