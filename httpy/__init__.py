"""HyperText Transfer Protocol, Python module
"""

from .status_codes import HTTPStatusCodes
from .client import HTTPClient, get, post, put, delete, head


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
    "__email__", "__author__", "__title__", "__url__", "__license__",
    "__date__", "__version__", "HTTPStatusCodes", "HTTPClient", "get",
    "post", "put", "head"
]
