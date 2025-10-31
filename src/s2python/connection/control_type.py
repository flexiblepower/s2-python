import abc

from s2python.common import EnergyManagementRole
from s2python.connection.async_.connection import S2AsyncConnection

class RoleHandler(abc.ABC):
    @abc.abstractmethod
    def get_s2_role(self) -> EnergyManagementRole: ...

    @abc.abstractmethod
    def register_handlers(self, connection: S2AsyncConnection) -> None: ...
