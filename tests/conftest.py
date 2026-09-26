import pytest
from alembic.config import Config
from alembic import command

@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    """Aplica todas as migrações do Alembic antes de iniciar a suíte de testes."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
