try:
    from fastapi import FastAPI
except ImportError as exc:
    raise ImportError(
        "The 'fastapi' package is required. Run 'pip install s2-python[fastapi]' to use this feature."
    ) from exc

from s2python.authorization.server import AbstractAuthServer
from s2python.generated.gen_s2_pairing import ConnectionDetails, ConnectionRequest, PairingResponse, PairingRequest


class FastAPIAuthServer(AbstractAuthServer):

    def handle_pairing_request(self, request_data: PairingRequest) -> PairingResponse:
        return PairingResponse()

    def handle_connection_request(self, request_data: ConnectionRequest) -> ConnectionDetails:
        return ConnectionDetails()


class MyFastAPI(FastAPI):

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.s2 = FastAPIAuthServer()


app = MyFastAPI()


@app.post('/requestConnection', response_model=ConnectionDetails)
async def post_request_connection(body: ConnectionRequest) -> ConnectionDetails:
    return app.s2.handle_connection_request(body)


@app.post('/requestPairing', response_model=PairingResponse)
async def post_request_pairing(body: PairingRequest) -> PairingResponse:
    return app.s2.handle_pairing_request(body)
