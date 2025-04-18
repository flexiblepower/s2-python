import argparse
import logging
import sys
from typing import Optional

from s2python.authorization.client import S2AbstractClient
from s2python.generated.gen_s2_pairing import (
    S2NodeDescription,
    Deployment,
    PairingToken,
    S2Role,
)

# Set up logging to show more details
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("test_pairing")


class TestPairingClient(S2AbstractClient):
    """Implementation of S2AbstractClient for testing the pairing process."""

    def solve_challenge(self, challenge: Optional[str] = None) -> str:
        """For testing purposes, we just return the challenge itself."""
        if challenge is None:
            if not self._connection_details or not self._connection_details.challenge:
                raise ValueError("Challenge not provided and not available in connection details")
            challenge = self._connection_details.challenge

        # For our mock server, we just return the challenge as is
        logger.info(f"Mock solving challenge: {challenge}")
        return challenge


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test S2 pairing with mock server")
    parser.add_argument(
        "--endpoint",
        type=str,
        default="http://localhost:8000/requestPairing",
        help="Rest endpoint to start S2 pairing. E.g. http://localhost:8000/requestPairing",
    )
    parser.add_argument(
        "--token",
        type=str,
        required=True,
        help="The pairing token shown by the mock server",
    )
    args = parser.parse_args()

    logger.info(f"Testing with endpoint: {args.endpoint}")
    logger.info(f"Using token: {args.token}")

    # Create node description
    node_description = S2NodeDescription(
        brand="Test Client",
        logoUri="http://example.com/logo.png",
        type="test client",
        modelName="S2 test client",
        userDefinedName="S2 Test Client",
        role=S2Role.RM,
        deployment=Deployment.LAN,
    )

    # Create the PairingToken object
    token = PairingToken(token=args.token)
    logger.info(f"Created PairingToken object: {token}")
    logger.info(f"PairingToken as dict: {token.model_dump()}")

    # Create a client to perform the pairing
    client = TestPairingClient(
        pairing_uri=args.endpoint,
        token=token,
        node_description=node_description,
        verify_certificate=False,
    )

    try:
        # Request pairing
        logger.info(f"Initiating pairing with endpoint: {args.endpoint}")
        pairing_response = client.request_pairing()
        logger.info(f"Pairing request successful: {pairing_response}")

        # Request connection details
        logger.info(f"Requesting connection from: {client.connection_request_uri}")
        connection_details = client.request_connection()
        logger.info(f"Connection request successful: {connection_details}")

        # Solve challenge
        challenge_result = client.solve_challenge()
        logger.info(f"Challenge solved successfully: {challenge_result}")

        logger.info("Test completed successfully!")

    except Exception as e:
        logger.error(f"Error during pairing process: {e}", exc_info=True)
