import re
from McClient.networking.Utils import get_server_info
# I like to store get_server_info
# in networking, since it is networking related, but I import it here, so
# it gets assigned to McClient.Utils namespace as well.


def __translate_escape(m):
    resolv = {
        "0": "\x1b[30m\x1b[21m",  # black
        "1": "\x1b[34m\x1b[21m",  # dark blue
        "2": "\x1b[32m\x1b[21m",  # dark green
        "3": "\x1b[36m\x1b[21m",  # dark cyan
        "4": "\x1b[31m\x1b[21m",  # dark red
        "5": "\x1b[35m\x1b[21m",  # purple
        "6": "\x1b[33m\x1b[21m",  # gold
        "7": "\x1b[37m\x1b[21m",  # gray
        "8": "\x1b[30m\x1b[1m",  # dark gray
        "9": "\x1b[34m\x1b[1m",  # blue
        "a": "\x1b[32m\x1b[1m",  # bright green
        "b": "\x1b[36m\x1b[1m",  # cyan
        "c": "\x1b[31m\x1b[1m",  # red
        "d": "\x1b[35m\x1b[1m",  # pink
        "e": "\x1b[33m\x1b[1m",  # yellow
        "f": "\x1b[37m\x1b[1m",  # white
        "k": "\x1b[5m",  # random
        "l": "\x1b[1m",  # bold
        "m": "\x1b[9m",  # strikethrough (escape code not widely supported)
        "n": "\x1b[4m",  # underline
        "o": "\x1b[3m",  # italic (escape code not widely supported)
        "r": "\x1b[0m"  # reset
    }
    c = m.group(1).lower()

    try:
        product = resolv[c]
    except KeyError:
        product = ""

    return product


def fix_message(s):
    return re.sub(ur"\xa7([0-9a-zA-Z])", __translate_escape, s) + "\x1b[0m"
