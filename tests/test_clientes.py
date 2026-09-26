import uuid
import pytest
from unittest.mock import AsyncMock, patch
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
@patch("app.services.cliente_service.get_cache", new_callable=AsyncMock)
@patch("app.services.cliente_service.set_cache", new_callable=AsyncMock)
@patch("app.services.cliente_service.delete_cache", new_callable=AsyncMock)
async def test_fluxo_completo_clientes(mock_del, mock_set, mock_get):
    mock_get.return_value = None  # Cache miss padrão

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        unique_suffix = uuid.uuid4().hex[:8]

        payload = {
            "nome": "Cliente Teste",
            "email": f"teste_{unique_suffix}@exemplo.com",
            "cpf": f"{uuid.uuid4().int}"[:11]
        }

        # 1. Criar Cliente (POST)
        res_post = await ac.post("/clientes", json=payload)
        assert res_post.status_code == 201
        data = res_post.json()
        cliente_id = data["id"]

        # 2. Buscar Cliente por ID (GET)
        res_get = await ac.get(f"/clientes/{cliente_id}")
        assert res_get.status_code == 200
        assert res_get.json()["id"] == cliente_id
        mock_set.assert_called_once()  # Garante gravação no cache

        # 3. Atualizar Cliente (PATCH)
        res_patch = await ac.patch(f"/clientes/{cliente_id}", json={"nome": "Nome Atualizado"})
        assert res_patch.status_code == 200
        assert res_patch.json()["nome"] == "Nome Atualizado"
        mock_del.assert_called_once()  # Invalidação de cache no update

        # 4. Deletar Cliente (DELETE)
        res_delete = await ac.delete(f"/clientes/{cliente_id}")
        assert res_delete.status_code == 204
        assert mock_del.call_count == 2  # Invalidação de cache no delete

        # 5. Confirmar Exclusão (GET 404)
        res_get_deleted = await ac.get(f"/clientes/{cliente_id}")
        assert res_get_deleted.status_code == 404
