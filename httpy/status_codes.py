""" HTTP Status Codes.

"""

from collections import namedtuple

# 1xx informational response
STATUS_CODES_INFORMATIONAL_RESPONSE = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Early Hints",
}

# 2xx successful
STATUS_CODES_SUCCESSFUL = {
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    208: "Already Reported",
    210: "Content Different",
    226: "IM Used",
}

# 3xx redirection
STATUS_CODES_REDIRECTION = {
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "Switch Proxy",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    310: "Too many Redirects",
}

# 4xx client errors
STATUS_CODES_CLIENT_ERRORS = {
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Time-out",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request-URI Too Long",
    415: "Unsupported Media Type",
    416: "Requested range unsatisfiable",
    417: "Expectation failed",
    418: "I'm a teapot",
    421: "Bad mapping/Misdirected Request",
    422: "Unprocessable entity",
    423: "Locked",
    424: "Method failure",
    425: "Unordered Collection",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    449: "Retry With",
    450: "Blocked by Windows Parental Controls",
    451: "Unavailable For Legal Reasons",
    456: "Unrecoverable Error",
    444: "No Response",
    495: "SSL Certificate Error",
    496: "SSL Certificate Required",
    497: "HTTP Request Sent to HTTPS Port",
    498: "Token expired/invalid",
    499: "Client Closed Request",
}

# 5xx server errors
STATUS_CODES_SERVER_ERRORS = {
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway ou Proxy Error",
    503: "Service Unavailable",
    504: "Gateway Time-out",
    505: "HTTP Version not supported",
    506: "Variant Also Negotiates",
    507: "Insufficient storage",
    508: "Loop detected",
    509: "Bandwidth Limit Exceeded",
    510: "Not extended",
    511: "Network authentication required",
    520: "Unknown Error",
    521: "Web Server Is Down",
    522: "Connection Timed Out",
    523: "Origin Is Unreachable",
    524: "A Timeout Occurred",
    525: "SSL Handshake Failed",
    526: "Invalid SSL Certificate",
    527: "Railgun Error",
}

# All HTTP status codes
HTTP_STATUS_CODES = {
    # 1xx informational response
    "1xx": STATUS_CODES_INFORMATIONAL_RESPONSE,
    # 2xx successful
    "2xx": STATUS_CODES_SUCCESSFUL,
    # 3xx redirection
    "3xx": STATUS_CODES_REDIRECTION,
    # 4xx client error
    "4xx": STATUS_CODES_CLIENT_ERRORS,
    # 5xx server error
    "5xx": STATUS_CODES_SERVER_ERRORS,
}


def _str2name(name):
    for char in " -/'":
        name = name.replace(char, "_")
    return name.upper()


class HTTPStatusCodes:
    """List of all HTTP status codes.

    """
    @staticmethod
    def category(_category):
        """Return the HTTP status codes for a specific category.

        """
        if not isinstance(_category, str):
            raise TypeError("_category is a str")

        if _category in HTTP_STATUS_CODES:
            return HTTP_STATUS_CODES[_category]

        raise TypeError("Invalid category")

    @staticmethod
    def message(code):
        """Returns HTTP status message.

        """
        code = int(code)
        for category in HTTP_STATUS_CODES:
            if code in HTTP_STATUS_CODES[category]:
                return HTTP_STATUS_CODES[category][code]
        return None

    @staticmethod
    def code(message):
        """Returns HTTP status message.

        """
        for category in HTTP_STATUS_CODES:
            values = list(HTTP_STATUS_CODES[category].values())
            keys = list(HTTP_STATUS_CODES[category].keys())
            if message in values:
                return keys[values.index(message)]
        return None


# This class represent a HTTP status code/message
_StatusCode = namedtuple('StatusCode', ['code', 'message'])

# Add list of categories to the HTTPStatusCodes class
setattr(HTTPStatusCodes, 'CATEGORIES', list(HTTP_STATUS_CODES.keys()))

# Add all HTTP status codes categories to the HTTPStatusCodes class
for _category in HTTP_STATUS_CODES:
    setattr(HTTPStatusCodes, 'CATEGORY_' +
            _category, HTTP_STATUS_CODES[_category])

# Add  all HTTP status messages to the HTTPStatusCodes class
for _category in HTTP_STATUS_CODES.values():
    for _code, msg in _category.items():
        setattr(HTTPStatusCodes, _str2name(msg), _StatusCode(_code, msg))
