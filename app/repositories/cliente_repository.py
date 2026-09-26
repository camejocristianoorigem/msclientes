from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.models import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


class ClienteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, page: int = 1, size: int = 10) -> List[Cliente]:
        offset = (page - 1) * size
        result = await self.db.execute(select(Cliente).offset(offset).limit(size))
        return result.scalars().all()

    async def get_by_id(self, cliente_id: UUID) -> Optional[Cliente]:
        result = await self.db.execute(select(Cliente).filter(Cliente.id == cliente_id))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[Cliente]:
        result = await self.db.execute(select(Cliente).filter(Cliente.email == email))
        return result.scalars().first()

    async def get_by_cpf(self, cpf: str) -> Optional[Cliente]:
        result = await self.db.execute(select(Cliente).filter(Cliente.cpf == cpf))
        return result.scalars().first()

    async def create(self, dto: ClienteCreate) -> Cliente:
        cliente = Cliente(**dto.model_dump())
        self.db.add(cliente)
        await self.db.commit()
        await self.db.refresh(cliente)
        return cliente

    async def update(self, cliente_id: UUID, dto: ClienteUpdate) -> Optional[Cliente]:
        cliente = await self.get_by_id(cliente_id)
        if not cliente:
            return None

        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(cliente, field, value)

        await self.db.commit()
        await self.db.refresh(cliente)
        return cliente

    async def delete(self, cliente_id: UUID) -> bool:
        cliente = await self.get_by_id(cliente_id)
        if not cliente:
            return False

        await self.db.delete(cliente)
        await self.db.commit()
        return True
