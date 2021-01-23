"""In this module, we define classes that implement the URLs.

"""

from collections import namedtuple

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
