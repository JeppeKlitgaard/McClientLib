McClientLib
===========

A library written in python, for python. It is (hopefully) very useful for making simple, as well as advanced MineCraft clients.

Protocols
=====
* 61 (1.5.2) ___This is the latest supported version.___
* 60 (1.5.0, 1.5.1) [Tag for v60](https://github.com/dkkline/McClientLib/tree/0.4.1)

Examples:
=====
* [DebugBot](https://github.com/dkkline/McClientLib/blob/master/examples/DebugBot.py)
* [pyCraft](https://github.com/dkkline/pyCraft)
* [Tutorial](https://github.com/dkkline/McClientLib/blob/master/examples/Tutorial.py)

Fun Facts:
=====
* You can read a book just by looking at someone holding it (They have to be within entity loading range, that's all)
* You can see which enchants a person has on, as long as they are within entity loading range (Exploit for PvP?)
* You can see how much air (Drowning) an entity has left, as long as they are within entity loading range
* Server can decide volume of sound effects (can be over 100%)
* Server can spawn as many particles as it wants to on clients (a lot!)
* Server can decide window name for windows.

Known Issues:
=====
* None, currently, this will change!

FAQ (Not actually asked yet, but I figured I could make a FAQ without you asking questions, no?):
=====
##### Q: How do I install it?
##### A: Like any other modern python module, via the setup.py or via pip. (If you still don't know how, see: [link](http://docs.python.org/2/install/), if you still don't know how, I recommend getting more familiar with python before using this module.)

##### Q: OMFG IT DONT WORK WTF BBQ GRILLED CHIKEN!?
##### A: Eh.

##### Q: I get kicked with "Outdated server!"
##### A: The version of this library is higher than the server you are connecting to. You have a few options.
###### 1.) Update the server.
###### 2.) Use the tag for that Protcol/MineCraft version. (See Protocols section) (Recommended if you cannot update server)
###### 3.) Look through the commit history for the right version (Messy)

##### Q: I get kicked with "Outdated client!"
##### A: The version of this library is lower than the server you are connecting to. Wait for the library to get updated, update it yourself (and push it to this git.), or backdate the server.

##### Q: How do I make a client?
##### A: See the tutorial further down this document, and the examples in the example folder.

##### Q: I get "Import Error: No module named McClient"
##### A: You forgot to actually install the module.

##### Q: How do I get the "server-list-ping" info (The stuff on the server-selection screen, e.g. MOTD, server-version, players, etc)?
##### A: `McClient.Utils.get_server_info(host, port)` returns a dict containing the information you want. Also see Tutorial section.

Tutorial:
=====
A McClientLib client can usually be done just by importing SimpleClient:

`Utils.get_server_info(host, port)` returns a dictionary containing all the info the client usually gets from the servers on the "server-selection" screen. The dict returned is:
* `protocol_version` is the version of the protocol the server uses. (e.g. '60')
* `server_version` is the version of the game the server uses. (e.g. '1.5')
* `motd` is the Message-Of-The-Day on the server, this should be decoded using `Utils.fix_message(message)`. (e.g. "A MineCraft Server.")
* `players` is the amount of players on the server. (e.g. "11")
* `max_players` is the maximum amount of players the server accepts. (e.g. "20")

`SimpleClient` Does a lot of amazing things for a quick and dirty client.
* Provides a default `EventManager` (You usually won't change this, use the eventmanager eventsystem instead)
* Provides a default `Receiver` (You should only change this if you're trying to connect to a modded server, that modifies networking classes (IE not one that uses the modern 0xFA packet), or you're trying to do something shady.
* Provides a default `Sender` (You should only change this if you're trying to connect to a modded server, that modifies networking classes (IE not one that uses the modern 0xFA packet), or you're trying to do something shady.
* Intelligently figures out if you want an `OfflineSession` or a real `Session`
Now to the actual programming, first I'd like to refer you to the Examples section, where you can find some example clients (Probably more useful then reading me ramble here in the Tutorial section!)

Start by importing SimpleClient, like so:
```python
from McClient import SimpleClient
from McClient import fix_message  # To decode minecraft messages, colors etc.
```

Simply make a client like so:
```python
client = SimpleClient()
```

Then you can "inject" whatever code you want into events. Like so:
```python
def display_message(message):
    print fix_message(message)

client.eventmanager.recv_chat_message.add_handler(display_message)
```

Now we're ready to connect:
```python
host = "localhost"
port = 25565
username = "dkkline"
password = "ThisIsn'tReallyMyPassword"
client.connect(host, port, username, password)
```
Tadaa! Now you should see it print whatever chat messages your client receives!

A better tutorial client, with less handholding:
Tutorial client: https://github.com/dkkline/McClientLib/blob/master/examples/Tutorial.py

Contact:
========
Dkkline (Me!):

Mail:       [jeppe@dapj.dk](mailto:jeppe@dapj.dk) - (I don't read mails frequently, but if you write to me here, you will get a response __eventually__ (TM).

Twitter:    [jeppeklitgaard](https://twitter.com/jeppeklitgaard) - (I don't read tweets frequently, but I can feel my inner tweetster growing, so I may use this more in the future. Or maybe not. Maybe.).
