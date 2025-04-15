from fastapi.testclient import TestClient

from s2python.authorization.fastapi_service import app


client = TestClient(app)


def test_post_pairing_request():
    response = client.post("/pairingRequest")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
