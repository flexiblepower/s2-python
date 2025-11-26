import abc


class S2ConnectionEvent(abc.ABC):
    pass


class ConnectionStarted(S2ConnectionEvent):
    pass

class ConnectionStopped(S2ConnectionEvent):
    pass
