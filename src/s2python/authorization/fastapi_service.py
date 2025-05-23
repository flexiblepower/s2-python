try:
    from fastapi import FastAPI
except ImportError as exc:
    raise ImportError(
        "The 'fastapi' package is required. Run 'pip install s2-python[fastapi]' to use this feature."
    ) from exc

from typing import Any

from s2python.authorization.default_server import S2DefaultServer
from s2python.generated.gen_s2_pairing import ConnectionDetails, ConnectionRequest, PairingResponse, PairingRequest


class S2FastAPI(FastAPI):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.s2 = S2DefaultServer()


app = S2FastAPI()


@app.post('/requestConnection', response_model=ConnectionDetails)
async def post_request_connection(body: ConnectionRequest) -> ConnectionDetails:
    return app.s2.handle_connection_request(body)


@app.post('/requestPairing', response_model=PairingResponse)
async def post_request_pairing(body: PairingRequest) -> PairingResponse:
    return app.s2.handle_pairing_request(body)
