McLib
=====

A MineCraft library written in, and for Python 2.7

Protocols
=====
* 39 (1.3.2)
* 47 (1.4.2)
* 49 (1.4.4, 1.4.5)

Examples:
=====
* DebugBot (https://github.com/dkkline/McLib/blob/master/examples/DebugBot/)

Fun Facts:
=====
* You can read a book just by looking at someone holding it (They have to be within entity loading range, that's all)
* You can see which enchants a person has on, as long as they are within entity loading range (Exploit for PvP?)
* You can see how much air (Drowning) an entity has left, as long as they are within entity loading range

Known Issues:
=====
* Sometimes will "fail to verify username", seems random. Just try again I guess :(
* Tutorial client (And other clients too I imagine) that use event03 will get weird looking messages when color codes are used

Tutorial:
=====
A McLib client should contain atleast these 4 classes:

* Connection (https://github.com/dkkline/McLib/blob/master/networking/Connection.py)
* PacketListener (https://github.com/dkkline/McLib/blob/master/networking/PacketListenerManager.py)
* PacketSender (https://github.com/dkkline/McLib/blob/master/networking/PacketSenderManager.py)
* EventManager (https://github.com/dkkline/McLib/blob/master/EventManager.py)

You could argue that that's a lot, but connecting to a MineCraft server is not just plug and play!
I'll go a bit more in depth.

`connection.py` contains a few classes actually, I'll try to explain them.

* `ServerConnection`, which is a class representing which is a class representing the connection between you and the MineCraft server.
* `EncryptedFileObjectHandler` and `EncryptedSocketObjectHandler`, You shouldn't have to worry about those, `ServerConnection` takes care of that!
* `SessionConnection`, which is a class representing the connection between you and `session.minecraft.net`,
This takes care of logging in, Keep-Alives etc.
* `KeepAliveConnection` which tells `session.minecraft.net` "Hey, yea, I'm still here!" every now and then, you shouldn't need to use this class, `SessionConnection` takes care of that.

Now to the actual programming, first I'd like to refer you to the Examples section, where you can find some example clients (Probably more useful then reading me ramble here in the Tutorial section!)

First we need a `SessionConnection`, this requires a username and a password. (Note below is psudo python code, you will need to import stuff etc, see Examples for that.)
```python
session = Connection.SessionConnection(username, password)
session.connect()
```
We just made a SessionConnection and told it to connect to `login.minecraft.net`.
Behind the scenes it also started a `KeepAliveConnection`

Next we want to set up a `sender` and a `listener`.
```python
sender = PacketSenderManager.Protocol_49()
listener = PacketListenerManager.Protocol_49()
```
We just made a `sender` and a `listener`, notice we took Protocol_49, this is the minecraft 1.4.4 and 1.4.5 protocol handler. (There should be a class for every (not snapshots/weekly builds) release since 1.3.2 (39)

Now that we're up and going on Protocol Handlers we need an `EventManager`, the purpose of eventmanagers is that you subclass the default one, and override the proper functions so you can react to events. You can see examples on this in the Example section. Let's say in this client we want to print every chat message we receive, I take a quick look at http://wiki.vg/Protocol, and find `Chat Message 0x03`, this tells me that I need to override `event03`, in the future I might make better function names, that have human readable names, but it is quite easy to look up on the wiki.
Now to the code:
```python
class MyEventManager(EventManager):
    def event03(self, direct, message):
        print "CHAT: %s" % message

eventmanager = MyEventManager()
```
We just made a custom eventmanager, and made a function that reacts to chat messages, and prints them!

Now to the final bit, this is getting quite lengthy!

```python
conn = Connection.ServerConnection(session, server_ip, server_port, sender, listener, event_manager=event_manager)
conn.connect()
```
Tadaa!! That is it!
The structure of most simple clients is exactly the same (More complicated clients could be putting a GUI on top, hell maybe even a full-blown minecraft client!), you just gotta override the appropriate functions in the eventmanager!

Tutorial client: https://github.com/dkkline/McLib/blob/master/examples/Tutorial/Tutorial.py

If you have a simple client, and will let me use it as an example, please tell me!