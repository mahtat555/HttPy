"""In this module, we define classes that implement the HTTP messages
(Requests and Response).

"""


class Request():
    """ Request class
    This class is used to create a valid HTTP Request.

    """


class Response():
    """ Response class
    This class is used to create a valid HTTP Response.

    """


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

    return start_line, headers, body


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
