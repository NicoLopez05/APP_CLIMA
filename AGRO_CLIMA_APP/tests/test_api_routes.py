import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_sensores():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/sensores/")
    assert response.status_code == 200
