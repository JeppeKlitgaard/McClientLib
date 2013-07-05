from networking import Session, OfflineSession
from networking import Receiver, Sender, Connection
from Events import EventManager


class SimpleClient(Connection):
    """Simplifies making a quick and dirty client."""
    def __init__(self):
        super(SimpleClient, self).__init__(None, EventManager,
                                           Receiver, Sender)

    def connect(self, host, port, username, password=None):
        """If password isn't specified, will use an OfflineSession."""
        if not password:
            session = OfflineSession()
        else:
            session = Session()
        session.connect(username, password)
        self.session = session

        super(SimpleClient, self).connect(host, port)
