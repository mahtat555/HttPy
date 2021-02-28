"""In this module, we define classes that implement the URLs.

"""

import re


from .errors import URLError


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


SACII_REGEX = re.compile(r"([\x00-\x7f]+)")


class URL:
    """ URL class

    This class represents the different elements of a URL, and some the
    methods used for manipulate these elements.

    """

    def __init__(self, url, params=None):
        # Encode the URL
        url = urlencode(url)
        self.url = url

        # Split the URL into (protocol, auth, host, path)
        self.urlsplit(url)

        # Add the parameters (query string) to the path
        if params:
            # split the path into (path, query, signet)
            path, query, signet = self.pathsplit()

            # Convert the query (params) from dict into str.
            if isinstance(params, dict):
                params = dict2query(params)

            if query:
                query += "&"
            query += params
            self.pathjoin(path, query, signet)

    def urlsplit(self, url):
        """ Parse a URL into its components.

        """
        # protocol
        try:
            protocol, access_path = url.split("://", 1)
            protocol = protocol.lower()
        except ValueError as cause:
            raise URLError("Invalid URL") from cause

        self.protocol = protocol

        # path
        if "/" in access_path:
            machine, path = access_path.split("/", 1)
        else:
            machine, path = access_path, ""
        self.path = "/" + path

        # auth = (user, password)
        if "@" in machine:
            auth, host = machine.split("@", 1)
            auth = tuple(auth.split(":"))
        else:
            host, auth = machine, None
        self.auth = auth

        # host = (domain, port)
        domain, port = host, None
        if ":" in host:
            domain, port = host.split(":", 1)
            port = int(port)
        elif protocol == "http":
            port = 80
        elif protocol == "https":
            port = 443

        self.host = (domain, port)

    def pathsplit(self):
        """ Parse a Path into its components.

        """
        signet = ""
        if "#" in self.path:
            self.path, signet = self.path.split('#', 1)

        query = ""
        if "?" in self.path:
            self.path, query = self.path.split('?', 1)

        return self.path, query, signet

    def pathjoin(self, path, query="", signet=""):
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

        self.path = path

    def __repr__(self):
        return "URL(protocol={}, auth={}, host={}, path={})".format(
            *map(repr, [self.protocol, self.auth, self.host, self.path])
        )


def query2dict(query):
    """Convert a query from string into Python dict.

    """

    query = query.split("&")
    _dict = {}
    for pair in query:
        key, value = pair.split("=", 1)
        _dict[key] = value

    return _dict


def dict2query(_dict, safe=b"", plus=False):
    """Convert a query from Python dict into string.

    """
    query = []

    if not isinstance(_dict, dict):
        raise TypeError("expected dict")

    for key, value in _dict.items():
        key = str(key)
        value = str(value)
        if plus:
            key = urlencode(key, safe=safe, plus=True)
            value = urlencode(value, safe=safe, plus=True)
        query.append("{}={}".format(key, value))

    # Encode the query string (params)
    query = "&".join(query)
    if not plus:
        query = urlencode(query, safe=safe, plus=False)
    return query


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


def urldecode(string, plus=False, encoding='utf-8', errors='replace'):
    """ The purpose of this function is to decode a URL.

    """

    # for decoding the content of an HTTP request
    if plus:
        string = string.replace("+", " ")

    data = SACII_REGEX.split(string)
    encode = [data[0]]

    for i in range(1, len(data), 2):
        encode.append(_urldecode(data[i]).decode(encoding, errors))
        encode.append(data[i + i])

    return "".join(encode)


def _urldecode(data):

    if isinstance(data, str):
        data = data.encode()

    data = data.split(b"%")
    result = [data[0]]

    for byte in data[1:]:
        try:
            char = HEX_BYTE[byte[:2]] + byte[2:]
        except KeyError:
            char = b"%" + byte
        result.append(char)

    return b"".join(result)
