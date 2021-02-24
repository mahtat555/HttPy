"""HyperText Transfer Protocol, Python module
"""

from .status_codes import HTTPStatusCodes
from .client import (
    # classes
    AsyncRequest, HttpRequest,

    # functions
    get, post, put, delete, head
)


# Author info
__email__ = "yassinmhtat@gmail.com"
__author__ = "MAHTAT Yassin"

# Project info
__title__ = "HyperText Transfer Protocol, Python implementation"
__url__ = "https://github.com/mahtat555/HttPy.git"
__license__ = "MIT"
__date__ = "2020-12-11"
__version__ = "0.0.1"

# List of public objects in this package
__all__ = [
    # project info and author info
    "__email__", "__author__", "__title__", "__url__", "__license__",
    "__date__", "__version__",

    # Classes
    "HTTPStatusCodes", "HttpRequest", "AsyncRequest",

    # functions
    "get", "post", "put", "head"
]
