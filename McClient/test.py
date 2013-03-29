from networking import Session, Connection
from Events import EventManager
from SimpleClient import SimpleClient

black_list = ["recv23", "recv21", "recv1F", "recv1C", "recv20", "recv28"]


def t(*args, **kwargs):
    pid = args[0]

    if not pid in black_list:
        print pid, kwargs


def t2(*args, **kwargs):
    print "TEST!!!\n"

HOST = "localhost"
PORT = 25565
with open(".credentials") as f:
    USERNAME, PASSWORD = f.read().split("\n")[:2]

connection = SimpleClient()
connection.eventmanager.got_event.add_handler(t)
connection.eventmanager.recv_keepalive.add_handler(t2)
connection.connect(HOST, PORT, USERNAME, PASSWORD)
