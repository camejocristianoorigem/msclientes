from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_db_session
from app.core.redis import get_cache, set_cache, delete_cache
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter()


class ClienteService:
    def __init__(self, db: AsyncSession):
        self.repo = ClienteRepository(db)

    async def listar(self, page: int, size: int) -> List[ClienteResponse]:
        clientes = await self.repo.get_all(page=page, size=size)
        return [ClienteResponse.model_validate(c) for c in clientes]

    async def criar(self, dto: ClienteCreate) -> ClienteResponse:
        if await self.repo.get_by_email(dto.email):
            raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
        if await self.repo.get_by_cpf(dto.cpf):
            raise HTTPException(status_code=400, detail="CPF já cadastrado.")

        cliente = await self.repo.create(dto)
        return ClienteResponse.model_validate(cliente)

    async def buscar_por_id(self, cliente_id: UUID) -> ClienteResponse:
        cache_key = f"cliente:{cliente_id}"
        cached = await get_cache(cache_key)
        if cached:
            return ClienteResponse.model_validate(cached)

        cliente = await self.repo.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")

        response_data = ClienteResponse.model_validate(cliente)
        await set_cache(cache_key, response_data.model_dump(mode="json"), ttl=300)
        return response_data

    async def atualizar(self, cliente_id: UUID, dto: ClienteUpdate) -> ClienteResponse:
        cliente = await self.repo.update(cliente_id, dto)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")

        await delete_cache(f"cliente:{cliente_id}")
        return ClienteResponse.model_validate(cliente)

    async def deletar(self, cliente_id: UUID) -> None:
        sucesso = await self.repo.delete(cliente_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")

        try:
            await delete_cache(f"cliente:{cliente_id}")
        except Exception:
            pass


@router.get("", response_model=List[ClienteResponse])
async def listar_clientes(
    skip: int = 0, 
    limit: int = 1000, 
    db: AsyncSession = Depends(get_db_session)
):
    page = (skip // limit) + 1 if limit > 0 else 1
    service = ClienteService(db)
    return await service.listar(page=page, size=limit)


@router.post("", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def criar_cliente(dto: ClienteCreate, db: AsyncSession = Depends(get_db_session)):
    service = ClienteService(db)
    return await service.criar(dto)


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def buscar_cliente(cliente_id: UUID, db: AsyncSession = Depends(get_db_session)):
    service = ClienteService(db)
    return await service.buscar_por_id(cliente_id)


@router.patch("/{cliente_id}", response_model=ClienteResponse)
async def atualizar_cliente(cliente_id: UUID, dto: ClienteUpdate, db: AsyncSession = Depends(get_db_session)):
    service = ClienteService(db)
    return await service.atualizar(cliente_id, dto)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_cliente(cliente_id: UUID, db: AsyncSession = Depends(get_db_session)):
    service = ClienteService(db)
    await service.deletar(cliente_id)
