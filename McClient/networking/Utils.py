import array
import string
from hashlib import sha1


def generate_serverID(serverID, secret, pubkey):
    hasher = sha1()
    hasher.update(serverID)
    hasher.update(secret)
    hasher.update(pubkey)

    return javaHexDigest(hasher)


# This function courtesy of barneygale
def javaHexDigest(digest):
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


def __translate_escape(m):
    c = m.group(1).lower()

    if   c == "0": return "\x1b[30m\x1b[21m" # black
    elif c == "1": return "\x1b[34m\x1b[21m" # dark blue
    elif c == "2": return "\x1b[32m\x1b[21m" # dark green
    elif c == "3": return "\x1b[36m\x1b[21m" # dark cyan
    elif c == "4": return "\x1b[31m\x1b[21m" # dark red
    elif c == "5": return "\x1b[35m\x1b[21m" # purple
    elif c == "6": return "\x1b[33m\x1b[21m" # gold
    elif c == "7": return "\x1b[37m\x1b[21m" # gray
    elif c == "8": return "\x1b[30m\x1b[1m"  # dark gray
    elif c == "9": return "\x1b[34m\x1b[1m"  # blue
    elif c == "a": return "\x1b[32m\x1b[1m"  # bright green
    elif c == "b": return "\x1b[36m\x1b[1m"  # cyan
    elif c == "c": return "\x1b[31m\x1b[1m"  # red
    elif c == "d": return "\x1b[35m\x1b[1m"  # pink
    elif c == "e": return "\x1b[33m\x1b[1m"  # yellow
    elif c == "f": return "\x1b[37m\x1b[1m"  # white
    elif c == "k": return "\x1b[5m"          # random
    elif c == "l": return "\x1b[1m"          # bold
    elif c == "m": return "\x1b[9m"          # strikethrough (escape code not widely supported)
    elif c == "n": return "\x1b[4m"          # underline
    elif c == "o": return "\x1b[3m"          # italic (escape code not widely supported)
    elif c == "r": return "\x1b[0m"          # reset

    return ""


def _translate_escapes(s):
    return re.sub(ur"\xa7([0-9a-zA-Z])", __translate_escape, s) + "\x1b[0m"


def fixChatMessage(message):
    return filter(lambda x: x in string.printable + "\x1b",
                  _translate_escapes(message))


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