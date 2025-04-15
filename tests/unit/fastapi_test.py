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


def test_post_connection_request():
    response = client.post("/requestConnection")
    assert response.status_code == 200
    assert response.json() == {
        "challenge": None,
        "connectionUri": None,
        "selectedProtocol": None,
    }
