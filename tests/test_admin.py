import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_default_admin_exists():
    async with AsyncClient(base_url="http://web:8000") as ac:
        response = await ac.post("/login", json={
            "email": "admin@example.com",
            "password": "admin"
        })
    
    # O login deve funcionar se o admin foi criado corretamente
    assert response.status_code == 200
    assert "token" in response.json()
