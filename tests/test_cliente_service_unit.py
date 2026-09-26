import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException

from app.services.cliente_service import ClienteService
from app.schemas.cliente import ClienteCreate


@pytest.mark.asyncio
@patch("app.services.cliente_service.ClienteRepository")
async def test_criar_cliente_email_duplicado_deve_lancar_excecao(mock_repo_cls):
    # Mock do repositório
    mock_repo = AsyncMock()
    mock_repo.get_by_email.return_value = {"id": "123", "email": "duplicado@exemplo.com"}
    mock_repo_cls.return_value = mock_repo

    db_mock = AsyncMock()
    service = ClienteService(db=db_mock)
    dto = ClienteCreate(nome="Teste", email="duplicado@exemplo.com", cpf="12345678900")

    with pytest.raises(HTTPException) as exc_info:
        await service.criar(dto)

    assert exc_info.value.status_code == 400
    assert "E-mail já cadastrado" in exc_info.value.detail
