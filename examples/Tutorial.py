import os
import sys
sys.path.append(os.path.join("..", "..", ".."))
# Please teach me the proper way!
# Forget all of the above, It's horrible code

from McLib.networking import Connection
# Contains ServerConnection and SessionConnection

from McLib.networking import PacketListenerManager
from McLib.networking import PacketSenderManager
# Our Protocol Handlers

from McLib import EventManager
# Our default EventManager
from getpass import getpass
# Function in standard python to get passwords the unixy way

username = raw_input("Username: ")
password = getpass()
# Get username and password

host = raw_input("Server (IP): ")
port = int(raw_input("Server (Port): "))  # Remember to turn to integer

session = Connection.SessionConnection(username, password)
session.connect()
# Create a connection to session.minecraft.net

sender = PacketSenderManager.Protocol_49()
listener = PacketListenerManager.Protocol_49()
# Create our Protocol Handlers, protocol version 49 (1.4.4 and 1.4.5)


class MyEventManager(EventManager.Protocol_49):
    def event03(self, direct, message):
        print "CHAT: %s" % message

    def eventFF(self, direct, reason):
        print "We got kicked: %s" % reason

event_manager = MyEventManager()
# Custom EventManager, override chat event.

con = Connection.ServerConnection(session, host, port, sender, listener,
                                  event_manager=event_manager)
con.connect()
# Server connection.