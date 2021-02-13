"""In this module, we define classes that implement the HTTP messages
(Requests and Response).

"""


import abc
from json import loads


class HTTPMessage:
    """ HTTPMessage class
    This class is used to create a valid HTTP Message (Request or Response).

    """

    def __init__(self, startline, headers, body):

        self.startline = startline
        self.headers = headers
        self.body = body

    def tostr(self):
        """ This function generates a valid HTTP message
        encoded in ASCII.

        """
        return tohttpmsg(self.startline, self.headers, self.body)

    async def fromstr(self, reader):
        """ This function converts an HTTP message encoded in ASCII
        into a Python object.

        """
        self.startline, self.headers, self.body = await fromreader(reader)

    @property
    def headers(self):
        """ Return the headers of an HTTP message.

        """
        return self.__headers

    @headers.setter
    def headers(self, _headers):
        """ Define the headers of an HTTP message.

        """
        if not isinstance(_headers, dict) and _headers:
            raise TypeError("expected dict")

        self.__headers = _headers

    @property
    def body(self):
        """ Return the body of an HTTP message

        """
        return self.__body

    @body.setter
    def body(self, _body):
        """ Define the body of an HTTP message.

        """
        if isinstance(_body, str):
            _body = _body.encode()

        if not isinstance(_body, bytes) and _body:
            raise TypeError("expected str or bytes")

        self.__body = _body

    def json(self):
        """ Returns the json-encoded content of a HTTP Message, if any

        """

        return loads(self.__body.replace(b"'", b'"'))

    @abc.abstractproperty
    def startline(self):
        """ abstract property
        Get and set the start line of an HTTP message.

        """


class Request(HTTPMessage):
    """ Request class
    This class is used to create a valid HTTP Request.

    """

    def __init__(self, method=None, path=None, version=None, headers=None,
                 body=None):

        super().__init__((method, path, version), headers, body)

    @property
    def startline(self):
        """ Return the start line of an HTTP request.

        """
        return self.method, self.path, self.version

    @startline.setter
    def startline(self, startline):
        """ Define the start line of an HTTP request.

        """
        self.method, self.path, self.version = startline

    def __repr__(self):
        return "<Request [{}]>".format(self.method)


class Response(HTTPMessage):
    """ Response class
    This class is used to create a valid HTTP Response.

    """

    def __init__(self, version=None, statuscode=None, statusmessage=None,
                 headers=None, body=None):

        super().__init__((version, statuscode, statusmessage), headers, body)

    @property
    def startline(self):
        """ Return the start line of an HTTP response.

        """
        return self.version, self.statuscode, self.statusmessage

    @startline.setter
    def startline(self, startline):
        """ Define the start line of an HTTP response.

        """
        self.version, self.statuscode, self.statusmessage = startline
        #self.statuscode = int(self.statuscode)

    def __repr__(self):
        return "<Response [{}]>".format(self.statuscode)


async def fromreader(reader):
    """This function converts data from an HTTP message (Request or Response)
    into a Python object.

    """
    # Start line
    line = await reader.readline()
    startline = line.split(maxsplit=2)

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

    return startline, headers, body


def tohttpmsg(start_line, headers, body=b""):
    """Create a valid HTTP message encoded in ASCII.

    """
    # Start line
    if not isinstance(start_line, (list, tuple)):
        raise TypeError("expected list or tuple")

    startline = []
    for value in start_line:
        if isinstance(value, bytes):
            value = value.decode()
        startline.append(value)

    startline = "{} {} {}".format(*startline).encode()

    # Headers
    if not isinstance(headers, dict):
        raise TypeError("expected dict")

    _headers = []
    for key, value in headers.items():
        if isinstance(key, bytes):
            key = key.decode()
        if isinstance(value, bytes):
            value = value.decode()
        _headers.append("{}: {}".format(key, value).encode())

    # Empty libe
    empty_line = b""

    # Body
    if isinstance(body, str):
        body = body.encode()

    if not isinstance(body, bytes):
        raise TypeError("expected bytes or str")

    return b"\r\n".join([startline, *_headers, empty_line, body])
