import json
import logging
from typing import Optional, TypeVar, Union, Type, Dict

from s2python.common import (
    Handshake,
    HandshakeResponse,
    InstructionStatusUpdate,
    PowerForecast,
    PowerMeasurement,
    ReceptionStatus,
    ResourceManagerDetails,
    RevokeObject,
    SelectControlType,
    SessionRequest,
)
from s2python.frbc import (
    FRBCActuatorStatus,
    FRBCFillLevelTargetProfile,
    FRBCInstruction,
    FRBCLeakageBehaviour,
    FRBCStorageStatus,
    FRBCSystemDescription,
    FRBCTimerStatus,
    FRBCUsageForecast,
)
from s2python.validate_values_mixin import S2Message
from s2python.s2_validation_error import S2ValidationError


LOGGER = logging.getLogger(__name__)
S2MessageType = str

M = TypeVar("M", bound=S2Message)


# May be generated with development_utilities/generate_s2_message_type_to_class.py
TYPE_TO_MESSAGE_CLASS: Dict[str, Type[S2Message]] = {
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
    @staticmethod
    def _parse_json_if_required(unparsed_message: Union[dict, str, bytes]) -> dict:
        if isinstance(unparsed_message, (str, bytes)):
            return json.loads(unparsed_message)
        return unparsed_message

    @staticmethod
    def parse_as_any_message(unparsed_message: Union[dict, str, bytes]) -> S2Message:
        """Parse the message as any S2 python message regardless of message type.

        :param unparsed_message: The message as a JSON-formatted string or as a json-parsed dictionary.
        :raises: S2ValidationError, json.JSONDecodeError
        :return: The parsed S2 message if no errors were found.
        """
        message_json = S2Parser._parse_json_if_required(unparsed_message)
        message_type = S2Parser.parse_message_type(message_json)

        if message_type not in TYPE_TO_MESSAGE_CLASS:
            raise S2ValidationError(
                None,
                message_json,
                f"Unable to parse {message_type} as an S2 message. Type unknown.",
                None,
            )

        return TYPE_TO_MESSAGE_CLASS[message_type].model_validate(message_json)

    @staticmethod
    def parse_as_message(unparsed_message: Union[dict, str, bytes], as_message: Type[M]) -> M:
        """Parse the message to a specific S2 python message.

        :param unparsed_message: The message as a JSON-formatted string or as a JSON-parsed dictionary.
        :param as_message: The type of message that is expected within the `message`
        :raises: S2ValidationError, json.JSONDecodeError
        :return: The parsed S2 message if no errors were found.
        """
        message_json = S2Parser._parse_json_if_required(unparsed_message)
        return as_message.from_dict(message_json)

    @staticmethod
    def parse_message_type(unparsed_message: Union[dict, str, bytes]) -> Optional[S2MessageType]:
        """Parse only the message type from the unparsed message.

        This is useful to call before `parse_as_message` to retrieve the message type and allows for strictly-typed
        parsing.

        :param unparsed_message: The message as a JSON-formatted string or as a JSON-parsed dictionary.
        :raises: json.JSONDecodeError
        :return: The parsed S2 message type if no errors were found.
        """
        message_json = S2Parser._parse_json_if_required(unparsed_message)

        return message_json.get("message_type")
