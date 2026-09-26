from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class ClienteBase(BaseModel):
    """Atributos compartilhados entre criação, atualização e leitura."""
    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do cliente")
    email: EmailStr = Field(..., description="E-mail válido e único")
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF contendo apenas dígitos ou formatado")


class ClienteCreate(ClienteBase):
    """Schema para o payload de criação (POST /clientes)."""
    pass


class ClienteUpdate(BaseModel):
    """Schema para atualização parcial (PATCH/PUT /clientes/{id})."""
    nome: str | None = Field(None, min_length=2, max_length=100)
    email: EmailStr | None = None
    ativo: bool | None = None


class ClienteResponse(ClienteBase):
    """Schema de retorno da API (Response DTO)."""
    id: UUID
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime

    model_config = {
        "from_attributes": True  # Permite mapeamento direto de objetos SQLAlchemy para Pydantic
    }

