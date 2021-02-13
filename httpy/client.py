""" client module

In this module, we will create the `HTTPClient` class which allows us to send a
valid request to an HTTP server and receive a valid response from it.

"""

import ssl

from .urls import urlsplit


class HTTPClient:
    """ HTTPClient class

    This category allows us to send a request to and receive a
    response from an HTTP server.

    """

    VERSION = "HTTP/1.1"

    def __init__(self, method="GET", url=None, headers=None, body=None):
        # split the URL into (protocol, auth, host, path)
        self.url = urlsplit(url)

        # Used SSL in the HTTPS protocol
        self.ssl_context = None
        # host = (domain, port)
        if self.url.host[1] == 443:
            self.ssl_context = ssl.SSLContext()

    async def connection(self):
        """ Create a connection to the HTTP server.

        """
        self.reader, self.writer = await asyncio.open_connection(
            *self.url.host, ssl=self.ssl_context)
