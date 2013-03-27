from DataTypes import TypeReader, TypeWriter
from Encryption import Socket
from threading import Thread
from NetworkHelper import NetworkHelper


class Connection(TypeReader, TypeWriter, Thread, NetworkHelper):
    """Represents a connection between a MineCraft server and client."""
    socket = None
    socket_file = None

    def __init__(self, session, eventmanager, receiver, sender,
                 host, port=25565):
        self.session = session
        self.eventmanager = eventmanager(self)
        self.receiver = receiver(self)
        self.sender = sender(self)
        self.host = host
        self.port = port

        secret = None

    def run(self):
        self.connect()

    def connect(self):
        """Connects to the given server."""
        self.socket = Socket()
        self.socket.connect(self.host, self.port)
        ### LOGIN ###
        self.sender.send_handshake()  # Send handshake(0x02)
        self.loop()

    def loop(self):
        while True:
            self.socket.wait4data()
            self.receiver.data_received()

    def read(self, *args, **kwargs):
        return self.socket.read(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.socket.send(*args, **kwargs)
