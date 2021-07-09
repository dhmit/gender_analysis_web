from app.common import HONORIFICS


def filter_honr(name):
    """
    Takes in a name and returns a version of the name without any honorifics.

    filter_honr("Miss. Woodhouse")
    >>> Woodhouse
    """
    name = name.split(' ')  # emma => [emma]
    return [n for n in name if (n not in HONORIFICS and n[:-1] not in HONORIFICS)]