from DataTypes import TypeReader, TypeWriter
from Encryption import Socket
from threading import Thread
from NetworkHelper import NetworkHelper


class Connection(TypeReader, TypeWriter, Thread, NetworkHelper):
    """Represents a connection between a MineCraft server and client."""
    socket = None
    socket_file = None

    def __init__(self, session, eventmanager, receiver, sender):
        Thread.__init__(self)
        self.session = session
        self.eventmanager = eventmanager(self)
        self.receiver = receiver(self)
        self.sender = sender(self)
        self.host = None
        self.port = None

        self.secret = None
        self.killed = False

    def run(self, *args, **kwargs):
        self.loop()

    def connect(self, host, port):
        """Connects to the given server."""
        self.host = host
        self.port = port

        self.socket = Socket()
        self.socket.connect(self.host, self.port)
        ### LOGIN ###
        self.sender.send_handshake()  # Send handshake(0x02)
        self.start()

    def loop(self):
        while not self.killed:
            self.socket.wait4data()
            self.receiver.data_received()

    def read(self, *args, **kwargs):
        return self.socket.read(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.socket.send(*args, **kwargs)

    def disconnect(self, reason="Connection closed.", timeout=10, force=False):
        if force:
            self.socket.close()
        else:
            self.killed = True
            self.join(timeout)
            self.sender.send_disconnect(reason)
            self.socket.close()
