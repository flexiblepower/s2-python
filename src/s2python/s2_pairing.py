import asyncio
import json
import logging
from dataclasses import dataclass

from s2python.generated.gen_s2_pairing import Protocols, S2NodeDescription


logger = logging.getLogger("s2python")

@dataclass
class S2PairingEndpoint:
    request_pairing_endpoint: str
    request_connection_endpoint: str
    

class S2Pairing:  # pylint: disable=too-many-instance-attributes
    publicKey: str
    privateKey: str
    pairing_endpoints: S2PairingEndpoint
    token: str
    s2ClientNodeId: str
    s2ClientNodeDescription: S2NodeDescription
    selectedProtocol: Protocols
    challenge: str
    paired: bool
    def __init__(  # pylint: disable=too-many-arguments
        self,
        publicKey: str,
        privateKey: str,
        pairing_endpoints: S2PairingEndpoint,
        token: str,
        s2ClientNodeId: str,
        s2ClientNodeDescription: S2NodeDescription,
        selectedProtocol: Protocols = Protocols.WebSocketSecure
    ) -> None:
      self.publicKey = publicKey
      self.privateKey = privateKey
      self.pairing_endpoints = pairing_endpoints
      self.token = token
      self.s2ClientNodeId = s2ClientNodeId
      self.s2ClientNodeDescription = s2ClientNodeDescription
      self.selectedProtocol = selectedProtocol
      
      self.challenge = None
      self.paired = false

    def pair() -> bool:
        return False