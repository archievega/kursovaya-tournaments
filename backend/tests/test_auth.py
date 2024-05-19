from httpx import AsyncClient, ASGITransport
from src.main import app


async def test_register(data):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/auth/register",
            json={
                "email": "user@example.com",
                "username": "some_user",
                "password": "stringstring"
            }
        )
        assert response.status_code == 201
        assert "id" in response.json()
        data["user_id"] = response.json()["id"]


async def test_login(data):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "username": "user@example.com",
                "password": "stringstring"
            }
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        data["token"] = response.json()["access_token"]


async def test_login_invalid_credentials():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "username": "wrong@wrong.com",
                "password": "wrongwrong"
            }
        )
    assert response.status_code == 400
    assert response.json() == {"detail": "LOGIN_BAD_CREDENTIALS"}
