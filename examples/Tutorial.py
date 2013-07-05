from McClient import SimpleClient
from McClient.Utils import fix_message

from getpass import getpass
# Function in standard python to get passwords the unixy way

username = raw_input("Username: ")
password = getpass()
# Get username and password

host = raw_input("Server (IP): ")
port = int(raw_input("Server (Port): "))  # Remember to turn to integer


class Events(object):
    @staticmethod
    def recv_chat_message(message):
        message = fix_message(message)  # Fix escapes, colors, etc
        print "CHAT: %s" % message

    @staticmethod
    def recv_client_disconnect(reason):
        print "We got kicked: %s" % reason

client = SimpleClient()
client.eventmanager.apply(Events())
client.connect(host, port, username, password)
# Server connection.

raw_input()  # Since connection runs in a seperate thread, we can't just CTRL-C
client.disconnect()  # We can call the wrapper function, disconnect, to nicely
# disconnect, it also has a force KWarg

# For a better chat client, see: https://github.com/dkkline/pyCraft
