"""
认证功能测试
"""
import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    """创建测试客户端"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_health_check(client):
    """测试健康检查"""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.anyio
async def test_register_validation():
    """测试注册参数验证"""
    from pydantic import ValidationError
    from app.schemas.auth import RegisterRequest

    # 测试密码太短
    with pytest.raises(ValidationError):
        RegisterRequest(
            username="testuser",
            email="test@example.com",
            password="123"  # 密码太短
        )

    # 测试无效邮箱
    with pytest.raises(ValidationError):
        RegisterRequest(
            username="testuser",
            email="not-an-email",
            password="password123"
        )
