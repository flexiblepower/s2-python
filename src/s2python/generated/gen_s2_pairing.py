"""
Generated classes based on s2-over-ip-pairing.yaml OpenAPI schema.
This file is auto-generated and should not be modified directly.
"""

import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional


class Protocols(str, Enum):
    """Supported protocol types."""

    WebSocketSecure = "WebSocketSecure"


class S2Role(str, Enum):
    """Roles in the S2 protocol."""

    CEM = "CEM"
    RM = "RM"


class Deployment(str, Enum):
    """Deployment types."""

    WAN = "WAN"
    LAN = "LAN"


@dataclass
class S2NodeDescription:
    """Description of an S2 node."""

    brand: Optional[str] = None
    logoUri: Optional[str] = None
    type: Optional[str] = None
    modelName: Optional[str] = None
    userDefinedName: Optional[str] = None
    role: Optional[S2Role] = None
    deployment: Optional[Deployment] = None


class PairingToken(str):
    """A token used for pairing.

    Must match pattern: ^[0-9a-zA-Z]{32}$
    """

    def __new__(cls, content: str):
        import re

        if not re.match(r"^[0-9a-zA-Z]{32}$", content):
            raise ValueError("PairingToken must be 32 alphanumeric characters")
        return super().__new__(cls, content)


@dataclass
class PairingInfo:
    """Information about a pairing."""

    pairingUri: Optional[str] = None
    token: Optional[PairingToken] = None
    validUntil: Optional[datetime] = None


@dataclass
class PairingRequest:
    """Request to initiate pairing."""

    token: Optional[PairingToken] = None
    publicKey: Optional[bytes] = None
    s2ClientNodeId: Optional[uuid.UUID] = None
    s2ClientNodeDescription: Optional[S2NodeDescription] = None
    supportedProtocols: Optional[List[Protocols]] = None


@dataclass
class PairingResponse:
    """Response to a pairing request."""

    s2ServerNodeId: Optional[uuid.UUID] = None
    serverNodeDescription: Optional[S2NodeDescription] = None
    requestConnectionUri: Optional[str] = None


@dataclass
class ConnectionRequest:
    """Request to establish a connection."""

    s2ClientNodeId: Optional[uuid.UUID] = None
    supportedProtocols: Optional[List[Protocols]] = None


@dataclass
class ConnectionDetails:
    """Details for establishing a connection."""

    selectedProtocol: Optional[Protocols] = None
    challenge: Optional[bytes] = None
    connectionUri: Optional[str] = None


# Serialization/Deserialization functions


def _is_dataclass_instance(obj):
    """Check if an object is a dataclass instance."""
    from dataclasses import is_dataclass

    return is_dataclass(obj) and not isinstance(obj, type)


def to_dict(obj):
    """Convert a dataclass instance to a dictionary."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, bytes):
        import base64

        return base64.b64encode(obj).decode("ascii")
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, list):
        return [to_dict(item) for item in obj]
    elif _is_dataclass_instance(obj):
        result = {}
        for field in obj.__dataclass_fields__:
            value = getattr(obj, field)
            if value is not None:
                result[field] = to_dict(value)
        return result
    else:
        return obj


def from_dict(cls, data):
    """Create a dataclass instance from a dictionary."""
    if data is None:
        return None

    if cls is datetime:
        return datetime.fromisoformat(data)
    elif cls is uuid.UUID:
        return uuid.UUID(data)
    elif cls is bytes:
        import base64

        return base64.b64decode(data.encode("ascii"))
    elif issubclass(cls, Enum):
        return cls(data)
    elif issubclass(cls, PairingToken):
        return PairingToken(data)
    elif hasattr(cls, "__dataclass_fields__"):
        fieldtypes = cls.__annotations__
        instance_data = {}

        for field, field_type in fieldtypes.items():
            if field in data and data[field] is not None:
                # Handle List[Type] annotations
                if hasattr(field_type, "__origin__") and field_type.__origin__ is list:
                    item_type = field_type.__args__[0]
                    instance_data[field] = [from_dict(item_type, item) for item in data[field]]
                else:
                    instance_data[field] = from_dict(field_type, data[field])

        return cls(**instance_data)
    else:
        return data
