from starlette import status

from tests.conftest import client


def test_health():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "OK !"}