import uuid

from s2python.generated.gen_s2_pairing import PairingResponse as GenPairingResponse

class PairingResponse(GenPairingResponse):
    model_config = GenPairingResponse.model_config
    model_config["validate_assignment"] = True
