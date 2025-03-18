import base64
import logging
import uuid
import datetime
from dataclasses import dataclass
from typing import Tuple, Union, Mapping, Any
import json
import requests

from jwskate import JweCompact, Jwk, Jwt, SignedJwt

from s2python.generated.gen_s2_pairing import (Protocols,
                                               PairingRequest,
                                               S2NodeDescription,
                                               PairingResponse,
                                               ConnectionRequest,
                                               ConnectionDetails)


logger = logging.getLogger("s2python")


REQTEST_TIMEOUT = 10
PAIRING_TIMEOUT = datetime.timedelta(minutes=5)
KEY_ALGORITHM = "RSA-OAEP-256"

@dataclass(frozen=True)
class PairingDetails:
    """The result of an S2 pairing
       :param pairing_response: Details about the server.
       :param connection_details: Details about how to connect.
       :param decrypted_challenge_base64: The decrypted challenge needed as bearer token."""
    pairing_response: PairingResponse
    connection_details: ConnectionDetails
    decrypted_challenge_base64: str

class S2Pairing:  # pylint: disable=too-many-instance-attributes
    _pairing_details: PairingDetails
    _paring_timestamp: datetime.datetime
    _request_pairing_endpoint: str
    _token: str
    _s2_client_node_description: S2NodeDescription
    _verify_certificate: Union[bool, str]
    _client_node_id: str
    _supported_protocols: Tuple[Protocols]
    def __init__(  # pylint: disable=too-many-arguments
        self,
        request_pairing_endpoint: str,
        token: str,
        s2_client_node_description: S2NodeDescription,
        verify_certificate: Union[bool, str] = False,
        client_node_id: str = str(uuid.uuid4()),
        supported_protocols: Tuple[Protocols] = (Protocols.WebSocketSecure, )
    ) -> None:
        """Creates an S2 pairing for the device and holds the challenge needed to be provided as bearer token
            when setting up an S2 (websockets) communication session
           :param request_pairing_endpoint: The full uri endpoint to request pairing from.
           :param token: The token that needs to be provided to the server in teh pairing process.
           :param s2_client_node_description: The descriptin ofr the client as a S2NodeDescription.
           :param verify_certificate: Either a boolean whether or not to verify the server's SSL certificate
                  (defaults to False), or a path to a certificate file to use for verification purposes.
           :param client_node_id: UUID for the client. If none is given, one will be generated.
           :param supported_protocols: The protocols supported by the client (defaults: Protocols.WebSocketSecure)."""
        self._paring_timestamp = datetime.datetime(year = datetime.MINYEAR, month = 1, day = 1)
        self._request_pairing_endpoint = request_pairing_endpoint
        self._token = token
        self._s2_client_node_description = s2_client_node_description
        self._verify_certificate = verify_certificate
        self._client_node_id = client_node_id
        self._supported_protocols = supported_protocols

    def _pair(self) -> None:
        """Private method establishing pairing"""
        # If pairing has been established recently we don't need to do it again
        if datetime.datetime.now() < (self._paring_timestamp + PAIRING_TIMEOUT):
            return

        self._paring_timestamp =  datetime.datetime.now()

        rsa_key_pair = Jwk.generate_for_alg(KEY_ALGORITHM).with_kid_thumbprint()
        pairing_request: PairingRequest = PairingRequest(token=self._token,
                                                        publicKey=rsa_key_pair.public_jwk().to_pem(),
                                                        s2ClientNodeId=self._client_node_id,
                                                        s2ClientNodeDescription=self._s2_client_node_description,
                                                        supportedProtocols=self._supported_protocols)

        response = requests.post(self._request_pairing_endpoint,
                                 json = pairing_request.dict(),
                                 timeout = REQTEST_TIMEOUT,
                                 verify = self._verify_certificate)
        response.raise_for_status()
        pairing_response: PairingResponse = PairingResponse.parse_raw(response.text)

        connection_request: ConnectionRequest = ConnectionRequest(s2ClientNodeId=self._client_node_id,
                                                                   supportedProtocols=self._supported_protocols)


        restest_pairing_uri: str = \
            pairing_response.requestConnectionUri if hasattr(pairing_response, 'requestConnectionUri') \
                                                  and pairing_response.requestConnectionUri is not None \
                                                  and pairing_response.requestConnectionUri != "" \
                                                  else self._request_pairing_endpoint.replace('requestPairing',
                                                                                              'requestConnection')

        logger.info('requestConnectionUri %s ', connection_details.connectionUri)

        response = requests.post(restest_pairing_uri,
                                 json = connection_request.dict(),
                                 timeout = REQTEST_TIMEOUT,
                                 verify = self._verify_certificate)
        response.raise_for_status()
        connection_details: ConnectionDetails = ConnectionDetails.parse_raw(response.text)
        # if websocket address doesn't start with ws:// or wss:// assume it's relative to the requestPairing
        if not connection_details.connectionUri.startswith('ws://') \
           and not connection_details.connectionUri.startswith('wss://'):
            connection_details.connectionUri = self._request_pairing_endpoint.replace('http://', 'ws://') \
                                                                             .replace('https://', 'wss://') \
                                                                             .replace('requestPairing', '') \
                                                                             + '/' + connection_details.connectionUri
        logger.info('connectionUri %s ', connection_details.connectionUri)

        challenge: Mapping[str, Any] = json.loads(JweCompact(connection_details.challenge).decrypt(rsa_key_pair))
        decrypted_challenge_token: SignedJwt = Jwt.unprotected(challenge)
        decrypted_challenge_str: str = base64.b64encode(bytes(decrypted_challenge_token)).decode('utf-8')
        self._pairing_details = PairingDetails(pairing_response, connection_details, decrypted_challenge_str)


    @property
    def pairing_details(self) -> PairingDetails:
        """:raises: requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError
           :return: PairingDetails object that's the result of the latest pairing."""
        self._pair()
        return self._pairing_details
