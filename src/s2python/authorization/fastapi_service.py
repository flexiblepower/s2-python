import requests

try:
    from fastapi import FastAPI
except ImportError as exc:
    raise ImportError(
        "The 'fastapi' package is required. Run 'pip install s2-python[fastapi]' to use this feature."
    ) from exc

from s2python.authorization.server import AbstractAuthServer
from s2python.generated.gen_s2_pairing import ConnectionDetails, ConnectionRequest, PairingResponse, PairingRequest


class FastAPIAuthServer(AbstractAuthServer, FastAPI):
    ...


app = FastAPIAuthServer()


@app.post('/requestConnection', response_model=ConnectionDetails)
async def post_request_connection(body: ConnectionRequest = None) -> ConnectionDetails:
    return app.handle_connection_request(body)


@app.post('/requestPairing', response_model=PairingResponse)
async def post_request_pairing(body: PairingRequest = None) -> PairingResponse:
    return app.handle_pairing_request(body)
