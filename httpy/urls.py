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
