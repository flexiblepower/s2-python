import argparse
import logging
import threading
import time
import os
import uuid

from s2python.authorization.default_client import S2DefaultClient
from s2python.authorization.default_http_server import S2DefaultHTTPServer
from s2python.authorization.default_ws_server import S2DefaultWSServer
from s2python.generated.gen_s2_pairing import (
    S2NodeDescription,
    Deployment,
    PairingToken,
    S2Role,
    Protocols,
)

logger = logging.getLogger("s2python")


def run_http_server(server):
    server.start_server()


def run_ws_server(server):
    server.start()


if __name__ == "__main__":
    # Configuration
    parser = argparse.ArgumentParser(description="S2 pairing example for FRBC RM")
    parser.add_argument("--pairing_endpoint", type=str, required=True)
    parser.add_argument("--pairing_token", type=str, required=True)

    args = parser.parse_args()

    pairing_endpoint = args.pairing_endpoint
    pairing_token = args.pairing_token

    # --- Client Setup ---
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
    client = S2DefaultClient(
        pairing_uri=pairing_endpoint,
        token=PairingToken(token=pairing_token),
        node_description=node_description,
        verify_certificate=False,
        supported_protocols=[Protocols.WebSocketSecure],
    )

    try:
        # Request pairing
        logger.info("Initiating pairing with endpoint: %s", pairing_endpoint)
        pairing_response = client.request_pairing()
        logger.info("Pairing request successful, requesting connection...")

        # Request connection details
        connection_details = client.request_connection()
        logger.info("Connection request successful")

        # Solve challenge
        challenge_result = client.solve_challenge()
        logger.info("Challenge solved successfully")

        # Establish secure connection
        s2_connection = client.establish_secure_connection()
        logger.info("Secure WebSocket connection established.")

        # Start S2 session with the connection details
        logger.info("Starting S2 session...")
        s2_connection.start()
        logger.info("S2 session is running. Press Ctrl+C to exit.")

        # Keep the main thread alive to allow the WebSocket connection to run.
        event = threading.Event()
        event.wait()

    except KeyboardInterrupt:
        logger.info("Program interrupted by user.")
    except Exception as e:
        logger.error("Error during pairing process: %s", e, exc_info=True)
        raise e
    finally:
        client.close_connection()
        logger.info("Connection closed.")
