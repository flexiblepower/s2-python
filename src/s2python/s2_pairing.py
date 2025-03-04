import logging
import uuid
from typing import List
import requests

from jwskate import JweCompact, Jwk
from jwskate.jwk.rsa import RSAJwk
from binapy.binapy import BinaPy

from s2python.generated.gen_s2_pairing import (Protocols,
                                               PairingRequest,
                                               S2NodeDescription,
                                               PairingResponse,
                                               ConnectionRequest,
                                               ConnectionDetails)


logger = logging.getLogger("s2python")

class S2Pairing:  # pylint: disable=too-many-instance-attributes
    _request_pairing_endpoint: str
    _token: str
    _s2_client_node_description: S2NodeDescription
    _s_client_node_id: str
    _timeout: int
    _supported_protocols: List[Protocols]
    rsa_key_pair: str
    paired: bool
    s2_server_node_id: str
    server_node_description: str
    selected_protocol: Protocols
    connection_uri: str
    challenge: BinaPy
    def __init__(  # pylint: disable=too-many-arguments
        self,
        request_pairing_endpoint: str,
        token: str,
        s2_client_node_description: S2NodeDescription,
        s_client_node_id: str = str(uuid.uuid4()),
        timeout: int = 10,
        supported_protocols: Protocols = None,
        rsa_key_pair: dict | RSAJwk = None,
    ) -> None:
        self._request_pairing_endpoint = request_pairing_endpoint
        self._token = token
        self._s2_client_node_description = s2_client_node_description
        self._s_client_node_id = s_client_node_id
        self.rsa_key_pair = rsa_key_pair
        self._timeout = timeout

        self._supported_protocols = supported_protocols if supported_protocols else [Protocols.WebSocketSecure]

        if self.rsa_key_pair is None: # generate keys if not set
            self.rsa_key_pair = Jwk.generate_for_alg("RSA-OAEP-256").with_kid_thumbprint()
        elif isinstance(self.rsa_key_pair, dict):
            self.rsa_key_pair = RSAJwk(self.rsa_key_pair)

        self.paired = False
        self.s2_server_node_id = None
        self.server_node_description = None
        self.selected_protocol = None
        self.connection_uri = None
        self.challenge = None

    def pair(self) -> bool:
        self.paired = False
        pairing_request: PairingRequest = PairingRequest(token=self._token,
                                                        publicKey=self.rsa_key_pair.public_jwk().to_pem(),
                                                        s2ClientNodeId=self._s_client_node_id,
                                                        s2ClientNodeDescription=self._s2_client_node_description,
                                                        supportedProtocols=self._supported_protocols)

        response = requests.post(self.request_pairing_endpoint,
                                 json=pairing_request.model_dump_json(),
                                 timeout=self._timeout)
        response.raise_for_status()
        pairing_response: PairingResponse = PairingResponse.parse_raw(response.json())
        self.s2_server_node_id = pairing_response.s2ServerNodeId
        self.server_node_description = pairing_response.serverNodeDescription

        connection_request: ConnectionRequest = ConnectionRequest(s2ClientNodeId=self._s_client_node_id,
                                                                   supportedProtocols=self._supported_protocols)

        response = requests.post(pairing_response.requestConnectionUri,
                                 json=connection_request.model_dump_json(),
                                 timeout=self._timeout)
        response.raise_for_status()
        connection_details: ConnectionDetails = ConnectionDetails.parse_raw(response.json())

        self.selected_protocol = connection_details.selectedProtocol
        self.connection_uri = connection_details.connectionUri
        self.challenge = JweCompact(connection_details.challenge).decrypt(self.rsa_key_pair)

        self.paired = True
        return self.paired
