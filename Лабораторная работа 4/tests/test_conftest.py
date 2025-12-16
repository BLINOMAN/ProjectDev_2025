
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_database_connection(test_db_session: AsyncSession):
    result = await test_db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

@pytest.mark.asyncio
async def test_user_repository_fixture(user_repository):
    assert user_repository is not None

@pytest.mark.asyncio
async def test_user_service_fixture(user_service):
    assert user_service is not None

@pytest.mark.asyncio
async def test_litestar_app_fixture(test_app):
    assert test_app is not None

@pytest.mark.asyncio
async def test_testclient_fixture(client):
    assert client is not None