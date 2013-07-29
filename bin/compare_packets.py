### VERY HACKY, VERY SCRIPTY, VERY VERY UGLY

import sys
import urllib2
import json
from McClient.Events import BaseEventManager as EventManager
from McClient import networking

if len(sys.argv) != 1:
    requested_version = sys.argv[1]
else:
    requested_version = raw_input("Version (e.g. '1.6.2'): ")

burger_url = "http://b.wiki.vg/json/{version}".format(version=requested_version)

burger_data = urllib2.urlopen(burger_url).read()

burger = json.loads(burger_data)[0]

eventmanager = EventManager()

###

print("McClient version: {}".format(networking.PROTOCOL_VERSION))
print("Burger version: {}\n".format(burger["version"]["protocol"]))

###

burger_packets = {"recv": set(),
                  "send": set()}
for packet in burger["packets"]["packet"].values():
    # Throw away 0x, add leading zero, make uppercase
    packet_id = hex(packet["id"])[2:].zfill(2).upper()  
    
    if packet["from_server"]:
        burger_packets["recv"].add(packet_id)
    if packet["from_client"]:
        burger_packets["send"].add(packet_id)

mcclient_packets = {"recv": set(),
                    "send": set()}
for event_name in eventmanager:
    if event_name.startswith("recv"):
        mcclient_packets["recv"].add(event_name[-2:])
    if event_name.startswith("sent"):
        mcclient_packets["send"].add(event_name[-2:])

for prefix in ("recv", "send"):
    print("===" + prefix.upper() + "===")
    # ^ = difference
    for difference in burger_packets[prefix] ^ mcclient_packets[prefix]:
        fmt = "{pid} (In burger: {ib}, In McClient: {imc})"
        in_burger = difference in burger_packets[prefix]
        in_mcclient = difference in mcclient_packets[prefix]
        print(fmt.format(pid=difference, ib=in_burger, imc=in_mcclient))
