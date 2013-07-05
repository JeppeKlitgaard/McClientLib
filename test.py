from McClient import SimpleClient
from getpass import getpass
import time

black_list = ["recv23", "recv21", "recv1F", "recv1C", "recv20", "recv28"]


def t(*args, **kwargs):
    pid = args[0]

    if not pid in black_list:
        print pid, kwargs

HOST = raw_input("HOST: ") or "localhost"
PORT = int(raw_input("PORT: ") or 25565)

try:
    with open(".credentials") as f:
        USERNAME, PASSWORD = f.read().split("\n")[:2]
except IOError:
    USERNAME = raw_input("Username: ")
    PASSWORD = getpass()

connection = SimpleClient()
connection.eventmanager.got_event.add_handler(t)
connection.connect(HOST, PORT, USERNAME, PASSWORD)

try:
    while True:
        # This is only needed because connection is in a seperate thread
        time.sleep(999)

except KeyboardInterrupt:
    connection.disconnect()
