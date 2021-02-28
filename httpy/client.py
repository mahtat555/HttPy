""" client module

In this module, we will create the `AsyncRequest` class which allows us to
send a valid request to an HTTP server and receive a valid response
from it asynchronously.

"""

import asyncio
import ssl
from json import dumps

from .urls import URL, dict2query
from .httpmessage import Request, Response
from .errors import ProtocolError, MethodError


class AsyncRequest:
    """ AsyncRequest class

    This class allows us to send a request to and receive a
    response from an HTTP server asynchronously.

    """

    # The version of our HTTP client
    VERSION = "HTTP/1.1"

    # We will use it to fetch (run) our requests
    loop = asyncio.get_event_loop()

    # methodes
    METHODES = ["GET", "POST", "PUT", "DELETE", "HEAD"]

    # protocols
    PROTOCOLS = ["http", "https"]

    def __init__(self, method, url, params=None, headers=None, data=None,
                 json=None, auth=None):

        # initialize our streams objects by `None`
        self.reader, self.writer = None, None

        # We use the `URL` class to represents the different
        # elements of this URL.
        self.url = URL(url, params)

        # Check if the method name given by the user is valid.
        if method not in self.METHODES:
            raise MethodError("Invalid Method Name !!")

        # Check if the protocol given by the user is valid.
        if self.url.protocol not in self.PROTOCOLS:
            raise ProtocolError("Invalid Protocol !!")

        # create the request
        self.request = Request(
            method, self.url.path, self.VERSION, {}, b"")

        # Define the headers of the request:
        headers = self.request.headers

        # add the Host to the headers
        headers.host(*self.url.host)

        # add the Connection to the headers
        headers.connection("close")

        # Define the content of the request:
        if json and not data:
            # Notify the server that it will receive JSON.
            headers.content_type("application/json")
            if not isinstance(json, (str, bytes)):
                json = dumps(json)
            self.request.body = json

        if data:
            # Notify the server that it will receive data from a form.
            headers.content_type("application/x-www-form-urlencoded")
            if not isinstance(data, (str, bytes)):
                data = dict2query(data, plus=True)
            self.request.body = data

        # add the HTTP message content length to the headers
        headers.content_length(len(self.request.body))

        # Authentication
        if auth is None:
            auth = self.url.auth
        # Add the Authorization
        if auth:
            headers.auth(auth)

    async def connection(self):
        """ Create a connection to the HTTP server.

        """
        # Create a new SSL context. for using it in the HTTPS protocol.
        ssl_context = None
        if self.url.protocol == "https":
            ssl_context = ssl.SSLContext()
        # Create a new connection to the server.
        self.reader, self.writer = await asyncio.open_connection(
            *self.url.host, ssl=ssl_context)

    async def send(self):
        """ Send an HTTP Request to an HTTP server

        """
        self.writer.write(self.request.tostr())

    async def recv(self, read_body=True):
        """ Receive a response from an HTTP server.

        """
        response = Response(reader=self.reader)
        await response.fromstr(read_body)
        if read_body:
            self.writer.close()
        return response

    async def fetch(self, read_body=True):
        """ Send an HTTP request and Receive a promise (response).

        """
        # Create the connection to the server
        await self.connection()
        # Send the request
        await self.send()
        # Recv the promise (response)
        return await self.recv(read_body)

    @staticmethod
    def fetchall(callbacks, loop=None, return_exceptions=False):
        """ Run awaitable requests in the callbacks sequence concurrently.
        And returns a promise

        """
        return asyncio.gather(
            *callbacks, loop=loop, return_exceptions=return_exceptions)

    def fetch_run(self):
        """ Send an HTTP request and Receive an HTTP response.

        """
        return self.run(self.fetch())

    @staticmethod
    def fetchall_run(callbacks, loop=None, return_exceptions=False):
        """ Run awaitable requests in the callbacks sequence concurrently.
        And return their responses

        """
        return AsyncRequest.run(AsyncRequest.fetchall(
            callbacks, loop=loop, return_exceptions=return_exceptions))

    @classmethod
    def run(cls, callback):
        """ Run a function create with the async/await keywords.

        """
        if cls.loop.is_closed():
            asyncio.set_event_loop(asyncio.new_event_loop())
            cls.loop = asyncio.get_event_loop()
            print("Create a new loop")
        return cls.loop.run_until_complete(callback)

    def close(self):
        """ Close the event loop.

        """
        self.loop.close()

    async def __aenter__(self):
        return await self.fetch(read_body=False)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()


############################
##  Asynchronous methods  ##
############################

def __asyncmethod(method, url, **kwargs):
    """ Send a request to a server, with a given method,
    and receive a response from it.

    """
    return AsyncRequest(method, url, **kwargs)


def asyncget(url, **kwargs):
    """ Send an HTTP request of type GET to an HTTP server, and receive
    an HTTP response from it.

    """
    return __asyncmethod("GET", url, **kwargs)


def asyncpost(url, **kwargs):
    """ Send an HTTP request of type POST to an HTTP server, and receive
    an HTTP response from it.

    """
    return __asyncmethod("POST", url, **kwargs)


def asyncput(url, **kwargs):
    """ Send an HTTP request of type PUT to an HTTP server, and receive
    an HTTP response from it.

    """
    return __asyncmethod("PUT", url, **kwargs)


def asyncdelete(url, **kwargs):
    """ Send an HTTP request of type DELETE to an HTTP server, and receive
    an HTTP response from it.

    """
    return __asyncmethod("DELETE", url, **kwargs)


def asynchead(url, **kwargs):
    """ Send an HTTP request of type HEAD to an HTTP server, and receive
    an HTTP response from it.

    """
    return __asyncmethod("HEAD", url, **kwargs)


###########################
##  Synchronous methods  ##
###########################

def __method(method, url, **kwargs):
    """ Send a request to a server, with a given method,
    and receive a response from it.

    """
    request = AsyncRequest(method, url, **kwargs)
    return request.fetch_run()


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
