""" In this module, we create some of the tools used in other modules.

"""


class _Data:
    """ This class  is meant to produce a string representation of
    the object's data.

    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def __str__(self):
        return type(self).__name__ + "({})".format(", ".join(
            ["{}='{}'".format(k, v) for k, v in self.__dict__.items()]
        ))

    def __repr__(self):
        return self.__str__()
