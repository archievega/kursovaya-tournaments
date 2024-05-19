from httpx import AsyncClient, ASGITransport
from src.main import app


async def test_create_tournament(data):
    headers = {'Authorization': f'Bearer {data["token"]}'}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/tournaments/create",
            headers=headers,
            json={
                "title": "test_tournament",
                "description": "test tournament description",
                "starts_at": "2024-05-19",
                "address": "test address",
                "max_players": 16
            }
        )
    assert response.status_code == 201
    assert "id" in response.json()
    data["tournament_id"] = response.json()["id"]


async def test_get_tournament(data):

    headers = {'Authorization': f'Bearer {data["token"]}'}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            f"/tournaments/{data['tournament_id']}",
            headers=headers
        )
    assert response.status_code == 200
    assert response.json()["title"] == "test_tournament"


async def test_join_tournament(data):
    headers = {'Authorization': f'Bearer {data["token"]}'}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            f"/tournaments/{data['tournament_id']}/join",
            headers=headers
        )
    assert response.status_code == 200
    players = response.json()['players']
    joined = False
    for player in players:
        if player['id'] == data['user_id']:
            joined = True
            break
    assert joined == True
                                 
