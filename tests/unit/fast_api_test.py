from fastapi.testclient import TestClient

from s2python.authorization.fastapi_service import MyFastAPI


client = TestClient(MyFastAPI)


def test_post_pairing_request():
    response = client.post("/pairingRequest")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
