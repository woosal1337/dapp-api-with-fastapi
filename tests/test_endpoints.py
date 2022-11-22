from starlette.testclient import TestClient
from app.main import app

from app.models.main import Admin, User


class TestEndpoints:
    def test_root(self):
        with TestClient(app) as client:
            response = client.get("/")
            assert response.status_code == 200
            assert response.json() == "Welcome to the API"

    def test_set_user(self):
        with TestClient(app) as client:
            test_data = User(publicAddress="0x777888999", firstName="John")

            response = client.post(
                "/set_user",
                json=test_data.json()
            )
            print(response.json())
            assert response.status_code == 200

