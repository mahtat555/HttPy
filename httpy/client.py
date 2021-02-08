""" client module

In this module, we will create the `HTTPClient` class which allows us to send a
valid request to an HTTP server and receive a valid response from it.

"""

from urls import urlsplit


class HTTPClient:
    """ HTTPClient class

    This category allows us to send a request to and receive a
    response from an HTTP server.

    """

    def __init__(self, url=None):
        self.url = url, urlsplit(url)
