# -*- coding: utf-8 -*-
from McClient.Utils import get_server_info as ping

host = raw_input("Host: ")
port = raw_input("Port(default: 25565): ")
if not port:
    port = 25565
else:
    port = int(port)

info = ping(host, port)

print "Players: {players}".format(players=info["players"])
print "Maximum players: {players}".format(players=info["max_players"])
print "Message of the Day: {motd}".format(motd=info["motd"])
print "Protocol version: {version}".format(version=info["protocol_version"])
print "MineCraft version: {version}".format(version=info["minecraft_version"])
