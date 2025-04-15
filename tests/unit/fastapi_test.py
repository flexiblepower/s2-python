from fastapi.testclient import TestClient

from s2python.authorization.fastapi_service import app


client = TestClient(app)


def test_post_pairing_request():
    response = client.post("/requestPairing")
    assert response.status_code == 200
    assert response.json() == {
        "requestConnectionUri": None,
        "s2ServerNodeId": None,
        "serverNodeDescription": None,
    }
