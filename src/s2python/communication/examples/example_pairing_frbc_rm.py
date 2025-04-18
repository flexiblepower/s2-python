import argparse
import uuid
import logging
import ssl
from typing import Optional

from s2python.communication.examples.example_frbc_rm import start_s2_session
from s2python.authorization.client import S2AbstractClient
from s2python.generated.gen_s2_pairing import (
    S2NodeDescription,
    Deployment,
    PairingToken,
    S2Role,
)

logger = logging.getLogger("s2python")


class S2PairingClient(S2AbstractClient):
    """Implementation of S2AbstractClient for pairing example."""

    def solve_challenge(self, challenge: Optional[str] = None) -> str:
        """Solve the challenge using the key pair."""
        return super().solve_challenge(challenge)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A simple S2 resource manager example."
    )
    parser.add_argument(
        "--endpoint",
        type=str,
        help="Rest endpoint to start S2 pairing. E.g. https://localhost/requestPairing",
    )
    parser.add_argument(
        "--pairing_token",
        type=str,
        help="The pairing token for the endpoint. You should get this from the S2 server e.g. ca14fda4",
    )
    parser.add_argument(
        "--verify-ssl",
        action="store_true",
        help="Verify SSL certificates (default: False)",
        default=False,
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Create node description
    node_description = S2NodeDescription(
        brand="TNO",
        logoUri="https://www.tno.nl/publish/pages/5604/tno-logo-1484x835_003_.jpg",
        type="demo frbc example",
        modelName="S2 pairing example stub",
        userDefinedName="TNO S2 pairing example for frbc",
        role=S2Role.RM,
        deployment=Deployment.LAN,
    )

    # Create a client to perform the pairing
    client = S2PairingClient(
        pairing_uri=args.endpoint,
        token=PairingToken(token=args.pairing_token, ),
        node_description=node_description,
        verify_certificate=args.verify_ssl,
    )

    try:
        # Request pairing
        logger.info("Initiating pairing with endpoint: %s", args.endpoint)
        pairing_response = client.request_pairing()
        logger.info("Pairing request successful, requesting connection...")

        # Request connection details
        connection_details = client.request_connection()
        logger.info("Connection request successful")

        # Solve challenge
        challenge_result = client.solve_challenge()
        logger.info("Challenge solved successfully")

        # Log connection details
        logger.info("Connection URI: %s", connection_details.connectionUri)

        # Start S2 session with the connection details
        logger.info("Starting S2 session...")
        start_s2_session(
            str(connection_details.connectionUri),
            bearer_token=challenge_result,
        )

    except Exception as e:
        logger.error("Error during pairing process: %s", e)
