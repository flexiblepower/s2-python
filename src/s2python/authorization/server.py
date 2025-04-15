from abc import ABC, abstractmethod
from typing import Any, Dict


class AbstractAuthServer(ABC):

    @abstractmethod
    def handle_pairing_request(self, request_data: Dict) -> Any:
        pass
