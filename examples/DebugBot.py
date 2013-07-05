from McClient import SimpleClient
from getpass import getpass


filter = [
    "recv00",  # keepalive
    "sent00",  # keepalive
    "recv04",  # time
]


def display_packet(name, *args, **kwargs):
    if name not in filter:
        print name, *args, **kwargs

username = raw_input("Username: ")
password = getpass()
host = raw_input("Host: ")
if not host:
    host = "localhost"
port = raw_input("Port: ")
if not port:
    port = 25565
port = int(port)

client = SimpleClient()
client.eventmanager.got_event.add_handler(display_packet)
client.connect(host, port, username, password)
