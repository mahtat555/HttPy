"""In this module, we define classes that implement the URLs.

"""

from collections import namedtuple


# These characters are always safe (not change) during the encoding process.
ALWAYS_SAFE = (
    b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    b'abcdefghijklmnopqrstuvwxyz'
    b'0123456789'
    b'_.-'
)


HEX_DIGITS = "0123456789abcdefABCDEF"

HEX_BYTE = dict(
    ((x + y).encode(), bytes.fromhex(x + y))
    for x in HEX_DIGITS for y in HEX_DIGITS
)

# Structured result objects
Path = namedtuple("Path", ("path", "query", "signet"))


class URL:
    """ URL class
    This class represents the different elements of a URL.

    """


def pathsplit(path):
    """ Parse a Path into its components.

    """
    signet = ""
    if "#" in path:
        path, signet = path.split('#', 1)

    query = ""
    if "?" in path:
        path, query = path.split('?', 1)

    return Path(path=path, query=query, signet=signet)


def pathjoin(path, query="", signet=""):
    """Combining path components into a path string.

    """
    if isinstance(path, bytes):
        path = path.decode()

    if isinstance(query, bytes):
        query = query.decode()

    if isinstance(signet, bytes):
        signet = signet.decode()

    if query:
        path += "?" + query

    if signet:
        path += "#" + signet

    return path


def query2dict(query):
    """Convert a query from string into Python dict.

    """

    query = query.split("&")
    _dict = {}
    for pair in query:
        key, value = pair.split("=", 1)
        _dict[key] = value

    return _dict


def dict2query(_dict):
    """Convert a query from Python dict into string.

    """
    query = []

    if not isinstance(_dict, dict):
        raise TypeError("expected dict")

    for key, value in _dict.items():
        query.append("{}={}".format(key, value))

    return "&".join(query)


def urlencode(data, safe=b"", plus=False):
    """ The purpose of this function is to encode a URL.

    """
    # for encoding the content of an HTTP request
    if plus:
        safe += b" "
    # for encoding URLs
    else:
        safe += b"!#$&'()*+,/:;=?@~?"

    if isinstance(data, str):
        data = data.encode()

    data = data.split(b"%")
    encode = _urlencode(data[0], safe)

    for _data in data[1:]:
        if _data[:2] in HEX_BYTE:
            encode += "%" + _data[:2].decode() + _urlencode(_data[2:], safe)
        else:
            encode += _urlencode(b"%" + _data, safe)

    return encode


def _urlencode(data, safe=b""):

    safe += ALWAYS_SAFE
    _data = ""

    for byte in data:
        if byte in safe:
            _data += chr(byte)
        else:
            _data += "%{0:02X}".format(byte)

    return _data.replace(" ", "+")
