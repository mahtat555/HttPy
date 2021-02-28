"""In this module, we define classes that implement the HTTP messages
(Requests and Response).

"""


import abc
from json import loads, decoder
from base64 import b64encode


class HTTPMessage:
    """ Asynchronous HTTP Message.
    This class is used to create a valid and async HTTP Message
    (Request or Response).

    """

    # In this status, the connection is created.
    # And we can read the status of the HTTP message.
    OPENED = 0

    # In this status, status is available.
    # And we can read the headers of the HTTP message.
    IN_HEADERS = 1

    # In this status, headers and status are available.
    # And we can read the body of the HTTP message.
    IN_BODY = 2

    # The operation is complete.
    # And the body of the HTTP message is available.
    DONE = 3

    def __init__(self, startline, headers, body, reader=None):

        self.startline = startline
        self.headers = headers
        self.body = body

        # The `readystate` property holds the status of our HTTP message.
        self.readystate = self.OPENED

        # This stream object used to read from the socket.
        self.reader = reader

    def tostr(self):
        """ This function generates a valid HTTP message
        encoded in ASCII.

        """
        # Start line
        # decodes the elements of `startline`
        startline = _bytestostr(*self.startline)
        startline = "{} {} {}".format(*startline).encode()

        # Headers
        _headers = []
        for key, value in self.headers.items():
            # convert the `key` and the `value` to str
            key, value = _bytestostr(key, value)
            _headers.append("{}: {}".format(key, value).encode())

        # Empty libe
        empty_line = b""

        return b"\r\n".join([startline, *_headers, empty_line, self.body])

    async def fromstr(self, read_body=True):
        """ This function converts an HTTP message encoded in ASCII
        into a Python object.

        """
        # Start line
        await self.__read_startline()

        # Headers
        await self.__read_headers()

        # Body
        if read_body:
            await self.read_body()

    async def __read_startline(self):
        """ The task of this function is to retrieve the
        start line of an HTTP message.

        """
        if self.readystate == self.OPENED:
            line = await self.reader.readline()
            startline = line.rstrip().split(maxsplit=2)
            # decodes the elements of `startline`
            self.startline = _bytestostr(*startline)
            self.readystate = self.IN_HEADERS

        return self.startline

    async def __read_headers(self):
        """ The task of this function is to retrieve the
        headers of an HTTP message.

        """
        if self.readystate == self.OPENED:
            self.__read_startline()

        if self.readystate == self.IN_HEADERS:
            headers = {}
            async for line in self.reader:
                line = line.rstrip()
                if not line:
                    break
                key, value = line.split(b":", 1)
                # convert the `key` and the `value` to str
                key, value = _bytestostr(key, value)
                headers[key] = value.strip()

            self.headers = headers
            self.readystate = self.IN_BODY

        return self.__headers

    async def read_body(self):
        """ The task of this function is to retrieve the
        body of an HTTP message.

        """
        if self.readystate == self.OPENED:
            self.__read_startline()

        if self.readystate == self.IN_HEADERS:
            self.__read_headers()

        if self.readystate == self.IN_BODY:
            self.body = await self.reader.read()
            self.readystate = self.DONE

        return self.body

    @property
    def headers(self):
        """ Return the headers of an HTTP message.

        """
        return self.__headers

    @headers.setter
    def headers(self, _headers):
        """ Define the headers of an HTTP message.

        """
        if _headers is None:
            _headers = {}

        if not isinstance(_headers, dict):
            raise TypeError("expected dict")

        self.__headers = Headers(_headers)

    @property
    def body(self):
        """ Return the body of an HTTP message

        """
        return self.__body

    @body.setter
    def body(self, _body):
        """ Define the body of an HTTP message.

        """
        if _body is None:
            _body = b""

        if isinstance(_body, str):
            _body = _body.encode()

        if not isinstance(_body, bytes):
            raise TypeError("expected str or bytes")

        self.__body = _body

    def json(self):
        """ Returns the json-encoded content of a HTTP Message, if any

        """
        try:
            return loads(self.__body)
        except decoder.JSONDecodeError:
            return loads(self.__body.replace(b"'", b'"'))

    @abc.abstractproperty
    def startline(self):
        """ abstract property
        Get and set the start line of an HTTP message.

        """


class Request(HTTPMessage):
    """ Asynchronous HTTP request.

    This class is used to create a valid and async HTTP Request.

    """

    def __init__(self, method=None, path=None, version=None, headers=None,
                 body=None, reader=None):

        super().__init__((method, path, version), headers, body, reader=reader)

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
                 headers=None, body=None, reader=None):

        super().__init__((version, statuscode, statusmessage), headers,
                         body, reader=reader)

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

        # convert the `statuscode` to int
        if self.statuscode:
            self.statuscode = int(self.statuscode)

    def __repr__(self):
        return "<Response [{}]>".format(self.statuscode)


class Headers(dict):
    """ Headers class
    This class is used to represent the different headers of a request.

    """

    def update(self, key, value):
        """ Update one of the headers.

        """
        super().__setitem__(key, value)

    def add(self, key, value, replace=False):
        """ Add a header into the headers.

        """
        if replace:
            self.update(key, value)
        elif key in self:
            raise KeyError(f"this key '{key}' already exists")
        else:
            super().__setitem__(key, value)

    def connection(self, value, replace=False):
        """ Add the Connection to the headers.

        """
        self.add("Connection", value, replace)

    def host(self, domain, port, replace=False):
        """ Add the Host to the headers.

        """
        host = str(domain)
        if port not in [80, 443]:
            host += ":" + str(port)

        self.add("Host", host, replace)

    def content_type(self, value):
        """ Add the content type to the headers.

        """
        self.add("Content-Type", value)

    def content_length(self, length):
        """ Add the content length to the headers.

        """
        self.add("Content-Length", length)

    def auth(self, auth):
        """ Add the `Authorization` header to the headers.

        """
        # decodes the username and password
        username, password = _bytestostr(*auth)

        authorization = "{}:{}".format(username, password)
        authorization = b64encode(authorization.encode())
        authorization = "Basic " + authorization.decode()

        self.add("Authorization", authorization)

    def __setitem__(self, key, value):
        raise TypeError("'Headers' object does not support item assignment")


def _bytestostr(*args):
    """ This function decodes a set of bytes to str.

    """

    if len(args) == 0:
        return None

    if len(args) == 1:
        if isinstance(args[0], bytes):
            return args[0].decode()
        return args

    decodes = []
    append = decodes.append

    for arg in args:
        if isinstance(arg, bytes):
            arg = arg.decode()
        append(arg)

    return decodes
