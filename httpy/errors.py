""" errors module

In this module, we will create some exceptions which allow us to
manage our errors in the project.

"""


class URLError(Exception):
    """ URLError class

    This class is used to handle exceptions in the `URL` class.

    """


class ProtocolError(URLError):
    """ ProtocolError class

    This class is used to handle exceptions in the `URL` class. Is raised
    if the protocol, used by the user, is not valid.

    """


class MethodError(URLError):
    """ MethodError class

    This class is used to handle exceptions in the `URL` class. Is raised
    if the method name, used by the user, is not valid.

    """
