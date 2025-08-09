# tests/test_main.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_root():
    # Usa ASGITransport para enviar requisições diretamente à app FastAPI
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "🚀 FastAPI + PostgreSQL funcionando!"}  # ← ajuste conforme o retorno real da sua API
