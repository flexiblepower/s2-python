import argparse
import uuid
import logging

from example_frbc_rm import start_s2_session
from s2python.s2_pairing import S2Pairing
from s2python.generated.gen_s2_pairing import S2NodeDescription, Deployment
from s2python.generated.gen_s2 import EnergyManagementRole

logger = logging.getLogger("s2python")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple S2 reseource manager example.")
    parser.add_argument('endpoint',
                        type=str,
                        help="Rest endpoint to start S2 pairing. E.g. https://localhost/requestPairing")
    parser.add_argument('pairing_token',
                        type=str,
                        help="The pairing toekn for teh endpoint. You should get this from the S2 server e.g. ca14fda4")
    args = parser.parse_args()

    nodeDescription: S2NodeDescription = \
        S2NodeDescription(brand="TNO",
                          logoUri = "https://www.tno.nl/publish/pages/5604/tno-logo-1484x835_003_.jpg",
                          type = "demo frbc example",
                          modelName = "S2 pairing example stub",
                          userDefinedName = "TNO S2 pairing example for frbc",
                          role = EnergyManagementRole.RM,
                          deployment = Deployment.LAN)
    client_node_id: str = str(uuid.uuid4())

    pairing: S2Pairing = S2Pairing(request_pairing_endpoint = args.endpoint,
                                   token = args.pairing_token,
                                   s2_client_node_description = nodeDescription,
                                   client_node_id = client_node_id)

    logger.info("Pairing details: \n%s", pairing.pairing_details)

    start_s2_session(pairing.pairing_details.connection_details.connectionUri,
                     bearer_token=pairing.pairing_details.decrypted_challenge)
