__all__ = (
    "HandlerError",
    "SessionError",
    "SessionBadLogin",
    "SessionVersionError",
    "NetworkError",
    "ConnectionClosed"
)


class HandlerError(Exception):
    pass


class SessionError(Exception):
    pass


class SessionBadLogin(SessionError):
    pass


class SessionVersionError(SessionError):
    pass


class NetworkError(Exception):
    pass


class ConnectionClosed(Exception):
    pass
