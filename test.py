from networking import Session, Connection
from Events import EventManager
from networking import Receiver, Sender
from getpass import getpass


def t(*args, **kwargs):
    print args, kwargs

session = Session()
passwd = getpass()
session.connect("dkkline", passwd)

eventmanager = EventManager
receiver = Receiver
sender = Sender

connection = Connection(session, eventmanager, receiver, sender,
                        "localhost", 25565)

connection.eventmanager.got_event.add_handler(t)
connection.run()
