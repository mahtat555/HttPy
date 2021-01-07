""" In this module, we create some of the tools used in other modules.

"""


class _Data:
    """ This class  is meant to produce a string representation of
    the object's data.

    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def add(self, key, value):
        """Add an attribute to the object.

        """
        self.__dict__[key] = value

    def adds(self, **kwargs):
        """Add attributes to the object.

        """
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def __str__(self):
        return type(self).__name__ + "({})".format(", ".join(
            ["{}='{}'".format(k, v) for k, v in self.__dict__.items()]
        ))

    def __repr__(self):
        return self.__str__()


async def fromreader(reader):
    """This function converts data from an HTTP message (Request or Response)
    into a Python object.

    """
    # Start line
    line = await reader.readline()
    start_line = line.split()

    # Headers
    headers = {}
    async for line in reader:
        line = line.rstrip()
        if not line:
            break
        key, value = line.split(b":", 1)
        headers[key] = value.strip()

    # Body
    body = await reader.read()

    HTTPMsg = type("HTTPMsg", (_Data,), {})
    return HTTPMsg(start_line=start_line, headers=headers, body=body)


def tohttpmsg(start_line, headers, body=b""):
    """Create a valid HTTP message encoded in ASCII.

    """
    # Start line
    if not isinstance(start_line, (list, tuple)):
        raise TypeError("expected list or tuple")

    start_line = "{} {} {}".format(*start_line).encode()

    # Headers
    if not isinstance(headers, dict):
        raise TypeError("expected dict")

    _headers = []
    for key, value in headers.items():
        _headers.append("{}: {}".format(key, value).encode())

    # Empty libe
    empty_line = b""

    # Body
    if isinstance(body, str):
        body = body.encode()

    if not isinstance(body, bytes):
        raise TypeError("expected bytes or str")

    return b"\r\n".join([start_line, *_headers, empty_line, body])
