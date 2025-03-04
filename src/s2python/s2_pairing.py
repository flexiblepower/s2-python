import logging
import uuid
import datetime
from typing import Tuple, Union
import requests

from jwskate import JweCompact
from jwskate.jwk.rsa import RSAJwk
from binapy.binapy import BinaPy

from s2python.generated.gen_s2_pairing import (Protocols,
                                               PairingRequest,
                                               S2NodeDescription,
                                               PairingResponse,
                                               ConnectionRequest,
                                               ConnectionDetails)


logger = logging.getLogger("s2python")

REQTEST_TIMEOUT = 10
CHALLANGE_TIMEOUT = datetime.timedelta(minutes=5)

class S2Pairing:  # pylint: disable=too-many-instance-attributes
    s2_server_node_id: str
    server_node_description: str
    selected_protocol: Protocols
    connection_uri: str
    _challenge: BinaPy

    _paring_timestamp: datetime.datetime
    _request_pairing_endpoint: str
    _token: str
    _s2_client_node_description: S2NodeDescription
    _verify_certificate: Union[bool, str]
    _client_node_id: str
    _supported_protocols: Tuple[Protocols]
    _rsa_key_pair: RSAJwk
    def __init__(  # pylint: disable=too-many-arguments
        self,
        request_pairing_endpoint: str,
        token: str,
        s2_client_node_description: S2NodeDescription,
        verify_certificate: Union[bool, str] = False,
        client_node_id: str = str(uuid.uuid4()),
        supported_protocols: Tuple[Protocols] = (Protocols.WebSocketSecure, )
    ) -> None:
        self._paring_timestamp = datetime.datetime(year = datetime.MINYEAR, month = 1, day = 1)
        self._request_pairing_endpoint = request_pairing_endpoint
        self._token = token
        self._s2_client_node_description = s2_client_node_description
        self._verify_certificate = verify_certificate
        self._client_node_id = client_node_id
        self._supported_protocols = supported_protocols
        self._rsa_key_pair = RSAJwk(self._rsa_key_pair)

    def get_challenge(self) -> BinaPy:
        # If pairing was done within the timeout, the existing chellange can be returned
        if (self._paring_timestamp + CHALLANGE_TIMEOUT) < datetime.datetime.now():
            return self._challenge

        self._paring_timestamp =  datetime.datetime.now()
        pairing_request: PairingRequest = PairingRequest(token=self._token,
                                                        publicKey=self._rsa_key_pair.public_jwk().to_pem(),
                                                        s2ClientNodeId=self._client_node_id,
                                                        s2ClientNodeDescription=self._s2_client_node_description,
                                                        supportedProtocols=self._supported_protocols)

        response = requests.post(self._request_pairing_endpoint,
                                 json=pairing_request.model_dump_json(),
                                 timeout=REQTEST_TIMEOUT,
                                 verify = self._verify_certificate)
        response.raise_for_status()
        pairing_response: PairingResponse = PairingResponse.parse_raw(response.json())
        self.s2_server_node_id = pairing_response.s2ServerNodeId
        self.server_node_description = pairing_response.serverNodeDescription

        connection_request: ConnectionRequest = ConnectionRequest(s2ClientNodeId=self._client_node_id,
                                                                   supportedProtocols=self._supported_protocols)

        response = requests.post(pairing_response.requestConnectionUri,
                                 json=connection_request.model_dump_json(),
                                 timeout=REQTEST_TIMEOUT,
                                 verify = self._verify_certificate)
        response.raise_for_status()
        connection_details: ConnectionDetails = ConnectionDetails.parse_raw(response.json())

        self.selected_protocol = connection_details.selectedProtocol
        self.connection_uri = connection_details.connectionUri
        self._challenge = JweCompact(connection_details.challenge).decrypt(self._rsa_key_pair)

        return self._challenge
