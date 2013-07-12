import array
import string
from hashlib import sha1
import socket
from struct import pack
from McClient.networking import PROTOCOL_VERSION


def generate_serverID(serverID, secret, pubkey):
    hasher = sha1()
    hasher.update(serverID)
    hasher.update(secret)
    hasher.update(pubkey)

    return java_digest(hasher)


# This function courtesy of barneygale
def java_digest(digest):
    d = long(digest.hexdigest(), 16)
    if d >> 39 * 4 & 0x8:
        d = "-%x" % ((-d) & (2 ** (40 * 4) - 1))
    else:
        d = "%x" % d
    return d


def hex2str(hex_num):
    return ''.join(["%02X " % ord(x) for x in hex_num]).strip()


def stringToByteArray(string):
    return array.array('B', string.decode("hex"))


# This function is also courtesy of barneygale
# https://gist.github.com/barneygale/1209061

def pack_string(string):
    """Packs a string."""
    return pack('>h', len(string)) + string.encode('utf-16be')


def get_server_info(host, port, timeout=3.0):
    """Returns the information the client receives when listing servers
    on the "server-selection" screen.

    WARNING: Strings are Unicode!

    The dict is contains:
        * protocol_version,
        * server_version,
        * motd,
        * players,
        * max_players
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((host, port))

    # Send 0xFE: Server list ping with 'magic' payload: "\x01"
    s.send("\xfe")
    s.send("\x01")

    # Send 0xFA plugin message
    s.send("\xfa")  # Packet identifier
    s.send(pack_string("MC|PingHost"))  # Message identifier
    s.send(pack(">h", 7 + 2 * len(host)))  # Payload length
    s.send(pack("b", PROTOCOL_VERSION))  # protocol version
    s.send(pack_string(host))  # host
    s.send(pack(">i", port))

    # Read as much data as we can, then close the socket.
    data = s.recv(1024)
    s.close()

    #Check we've got a 0xFF Disconnect
    assert data[0] == '\xff'

    #Remove: packet ident (0xFF), short containing the length of the string
    data = data[3:]  # packet ident: 1 byte, short: 2 bytes, total: 3 bytes
    #Decode UCS-2 string
    data = data.decode('utf-16be')

    # Check that the first 3 characters were what we expected.
    # Then throw them away.
    assert data[:3] == u"\xa7\x31\x00"
    data = data[3:]

    # Split
    data = data.split("\x00")

    return {"protocol_version": int(data[0]),
            "minecraft_version": data[1],
            "motd": data[2],
            "players": int(data[3]),
            "max_players": int(data[4])}


def TwosCompliment(digest):
    carry = True
    for i in range((digest.__len__() - 1), -1, -1):
        value = 255 - digest[i]
        digest[i] = value
        if(carry):
            carry = digest[i] == 0xFF
            digest[i] = digest[i] + 1
    return digest


def trimStart(string, character):
    for c in string:
        if (c == character):
            string = string[1:]
        else:
            break
    return string


def getHexString(byteArray):
    result = ""
    for i in range(byteArray.__len__()):
        if (byteArray[i] < 0x10):
            result += '0'
        result += hex(byteArray[i])[2:]
    return result


def unpackNbt(tag):
    """Unpack an NBT tag into a native Python data structure."""
    if isinstance(tag, TAG_List):
        return [unpack_nbt(i) for i in tag.tags]
    elif isinstance(tag, TAG_Compound):
        return dict((i.name, unpack_nbt(i)) for i in tag.tags)
    else:
        return tag.value


def packNbt(s):
    """
    Pack a native Python data structure into an NBT tag. Only the following
    structures and types are supported:

     * int
     * float
     * str
     * unicode
     * dict

    Additionally, arbitrary iterables are supported.

    Packing is not lossless. In order to avoid data loss, TAG_Long and
    TAG_Double are preferred over the less precise numerical formats.

    Lists and tuples may become dicts on unpacking if they were not homogenous
    during packing, as a side-effect of NBT's format. Nothing can be done
    about this.

    Only strings are supported as keys for dicts and other mapping types. If
    your keys are not strings, they will be coerced. (Resistance is futile.)
    """

    if isinstance(s, int):
        return TAG_Long(s)
    elif isinstance(s, float):
        return TAG_Double(s)
    elif isinstance(s, (str, unicode)):
        return TAG_String(s)
    elif isinstance(s, dict):
        tag = TAG_Compound()
        for k, v in s:
            v = pack_nbt(v)
            v.name = str(k)
            tag.tags.append(v)
        return tag
    elif hasattr(s, "__iter__"):
        # We arrive at a slight quandry. NBT lists must be homogenous, unlike
        # Python lists. NBT compounds work, but require unique names for every
        # entry. On the plus side, this technique should work for arbitrary
        # iterables as well.
        tags = [pack_nbt(i) for i in s]
        t = type(tags[0])
        # If we're homogenous...
        if all(t == type(i) for i in tags):
            tag = TAG_List(type=t)
            tag.tags = tags
        else:
            tag = TAG_Compound()
            for i, item in enumerate(tags):
                item.name = str(i)
            tag.tags = tags
        return tag
    else:
        raise ValueError("Couldn't serialise type %s!" % type(s))
