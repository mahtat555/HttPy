""" client module

In this module, we will create the `HTTPClient` class which allows us to send a
valid request to an HTTP server and receive a valid response from it.

"""

import asyncio
import ssl

from .urls import URL
from .httpmessage import Request, Response
from .errors import ProtocolError, MethodError


class HTTPClient:
    """ HTTPClient class

    This class allows us to send a request to and receive a
    response from an HTTP server.

    """

    # The version of our HTTP client
    VERSION = "HTTP/1.1"

    # We will use it to fetch (run) our requests
    loop = asyncio.get_event_loop()

    # methodes
    METHODES = ["GET", "POST", "PUT", "DELETE", "HEAD"]

    # protocols
    PROTOCOLS = ["http", "https"]

    def __init__(self, method, url, headers=None, body=None):
        # URL
        self.url = URL(url)

        # method
        if method not in self.METHODES:
            raise MethodError("Invalid Method Name !!")

        # protocol
        if self.url.protocol not in self.PROTOCOLS:
            raise ProtocolError("Invalid Protocol !!")

        # Used SSL in the HTTPS protocol
        self.ssl_context = None
        # host = (domain, port)
        host, port = self.url.host
        if port == 443:
            self.ssl_context = ssl.SSLContext()

        # Prepare the request
        # headers
        if headers is None:
            headers = {}
        if "Connection" not in headers:
            headers["Connection"] = "close"
        if "Host" not in headers:
            headers["Host"] = host
            if port not in (80, 443):
                headers["Host"] += ": " + str(port)

        # Notify the server that it will receive JSON.

        # body
        if body is None:
            body = b""

        # create the request
        self.request = Request(
            method, self.url.path, self.VERSION, headers, body)

    async def connection(self):
        """ Create a connection to the HTTP server.

        """
        self.reader, self.writer = await asyncio.open_connection(
            *self.url.host, ssl=self.ssl_context)

    async def send(self):
        """ Send an HTTP Request to an HTTP server

        """
        self.writer.write(self.request.tostr())

    async def recv(self):
        """ Receive a response from an HTTP server.

        """
        response = Response()
        await response.fromstr(self.reader)
        self.writer.close()
        return response

    async def call(self):
        """ Send request and Receive response

        """
        # Create the connection to the server
        await self.connection()
        # Send the request
        await self.send()
        # Recv the response
        return await self.recv()

    def fetch(self):
        """ Send request and Receive response

        """
        return self.run(self.call())

    def run(self, function):
        """ Run a function create with the async/await keywords.

        """
        return self.loop.run_until_complete(function)

    def close(self):
        """ Close the event loop.

        """
        self.loop.close()


def __method(method, url, **kwargs):
    """ Send a request to a server, with a given method,
    and receive a response from it.

    """
    request = HTTPClient(method, url, **kwargs)
    return request.fetch()


def get(url, **kwargs):
    """ Send an HTTP request of type GET to an HTTP server, and receive
    an HTTP response from it.

    """
    return __method("GET", url, **kwargs)


def post(url, **kwargs):
    """ Send an HTTP request of type POST to an HTTP server, and receive
    an HTTP response from it.

    """
    return __method("POST", url, **kwargs)


def put(url, **kwargs):
    """ Send an HTTP request of type PUT to an HTTP server, and receive
    an HTTP response from it.

    """
    return __method("PUT", url, **kwargs)


def delete(url, **kwargs):
    """ Send an HTTP request of type DELETE to an HTTP server, and receive
    an HTTP response from it.

    """
    return __method("DELETE", url, **kwargs)


def head(url, **kwargs):
    """ Send an HTTP request of type HEAD to an HTTP server, and receive
    an HTTP response from it.

    """
    return __method("HEAD", url, **kwargs)
