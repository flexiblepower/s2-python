import requests

try:
    from fastapi import FastAPI
except ImportError as exc:
    raise ImportError(
        "The 'fastapi' package is required. Run 'pip install s2-python[fastapi]' to use this feature."
    ) from exc

from s2python.authorization.server import AbstractAuthServer


class FastAPIAuthServer(AbstractAuthServer, FastAPI):
    ...


app = FastAPIAuthServer()


@app.get("requestPairing/")
async def root(request_data):
    pairing_response = app.handle_pairing_request(request_data)
    return pairing_response
