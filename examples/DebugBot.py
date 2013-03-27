import os
import sys
sys.path.append(os.path.join("..", "..", ".."))  # I realize this is probably
# The wrong way to do it, this "Bot" is only used for debugging tho
from McLib.networking import Connection
from McLib.networking import PacketListenerManager
from McLib.networking import PacketSenderManager
from DebugEventManager import DebugEventManager, CustomFilter
from getpass import getpass

## Filters:
f_keep_alive = ["00"]

f_time = ["04"]

f_chunk = ["38",
           "34"]

f_entity = ["15",
            "18",
            "21",
            "20",
            "22",
            "23",
            "1C",
            "1D",
            "1F"]

f_inventory = ["67",
               "68"]

f_sound = ["3D",
           "3E"]

f_block = ["35",
           "84"]


## Set up actual filter
filter = []
#filter.extend(f_entity)
#filter.extend(f_chunk)
#filter.extend(f_time)
#filter.extend(f_keep_alive)
#filter.extend(f_inventory)
#filter.extend(f_sound)
#filter.extend(f_block)
## End of Filters

username = raw_input("Username: ")
password = getpass()

session = Connection.SessionConnection(username, password)
session.connect()

sender = PacketSenderManager.get_protocol(49)
sender = sender()

listener = PacketListenerManager.get_protocol(49)
listener = listener()

custom_filter = CustomFilter()
custom_filter.set_up_filter(filter)

EventManager = DebugEventManager(custom_filter)
server = Connection.ServerConnection(session, "localhost", 25565,
                                     sender, listener,
                                     event_manager=EventManager)
server.connect()
