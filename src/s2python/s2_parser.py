import json
import logging
from typing import Optional, TypeVar

from s2python.validate_values_mixin import ValidateValuesMixin
from s2python.s2_validation_error import S2ValidationError
from s2python.common import *
from s2python.frbc import *

LOGGER = logging.getLogger(__name__)
MessageType = str
S2Message = ValidateValuesMixin

C = TypeVar("C", bound=S2Message)


# May be generated with development_utilities/generate_s2_message_type_to_class.py
TYPE_TO_MESSAGE_CLASS = {
    "FRBC.ActuatorStatus": FRBCActuatorStatus,
    "FRBC.FillLevelTargetProfile": FRBCFillLevelTargetProfile,
    "FRBC.Instruction": FRBCInstruction,
    "FRBC.LeakageBehaviour": FRBCLeakageBehaviour,
    "FRBC.StorageStatus": FRBCStorageStatus,
    "FRBC.SystemDescription": FRBCSystemDescription,
    "FRBC.TimerStatus": FRBCTimerStatus,
    "FRBC.UsageForecast": FRBCUsageForecast,
    "Handshake": Handshake,
    "HandshakeResponse": HandshakeResponse,
    "InstructionStatusUpdate": InstructionStatusUpdate,
    "PowerForecast": PowerForecast,
    "PowerMeasurement": PowerMeasurement,
    "ReceptionStatus": ReceptionStatus,
    "ResourceManagerDetails": ResourceManagerDetails,
    "RevokeObject": RevokeObject,
    "SelectControlType": SelectControlType,
    "SessionRequest": SessionRequest,
}


class S2Parser:
    def __init__(self):
        pass

    def parse_str_as_any_message(self, message_str: str) -> S2Message:
        message_dict = json.loads(message_str)
        message_type = self.get_message_type_from_dict(message_dict)

        if message_type not in TYPE_TO_MESSAGE_CLASS:
            raise S2ValidationError(
                message_dict,
                f"Unable to parse {message_type} as an S2 message. Type unknown.",
            )

        return TYPE_TO_MESSAGE_CLASS[message_type].parse_obj(message_str)

    def parse_dict_as_any_message(self, message_dict: dict) -> S2Message:
        message_type = self.get_message_type_from_dict(message_dict)

        if message_type not in TYPE_TO_MESSAGE_CLASS:
            raise S2ValidationError(
                message_dict,
                f"Unable to parse {message_type} as an S2 message. Type unknown.",
            )

        return TYPE_TO_MESSAGE_CLASS[message_type].parse_obj(message_dict)

    def parse_str_as_message(self, message: str, as_message: S2Message[C]) -> C:
        """Parse the message to a specific S2 python message.

        :param message: The message as a JSON-formatted string.
        :param as_message: The type of message that is expected within the `message`
        :raises: S2ValidationError
        :return: The parsed message if no errors were found.
        """
        return as_message.from_json(message)

    def parse_dict_as_message(self, message: dict, as_message: S2Message[C]) -> C:
        """Parse the message to a specific S2 python message.

        :param message: The message as a dictionary.
        :param as_message: The type of message that is expected within the `message`
        :raises: S2ValidationError
        :return: The parsed message if no errors were found.
        """
        return as_message.from_dict(message)

    def get_message_type_from_str(self, message: str) -> Optional[MessageType]:
        return json.loads(message).get("message_type")

    def get_message_type_from_dict(self, message: dict) -> Optional[MessageType]:
        return message.get("message_type")
