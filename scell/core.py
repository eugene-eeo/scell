"""
    scell.core
    ~~~~~~~~~~

    Provides abstractions over lower level APIs and
    file objects and their interests.
"""


from select import select as _select
from collections import namedtuple


def select(rl, wl, timeout=None):
    """
    Returns the file objects ready for reading/writing
    from the read-list (*rl*) and write-list (*wl*),
    subject to *timeout* in seconds.

    :param rl: Objects interested in readability.
    :param wl: Objects interested in writability.
    :param timeout: Maximum blocking time in seconds,
        *None* for no timeout.
    """
    if not (rl or wl):
        return [], []
    readers, writers, _ = _select(rl, wl, (), timeout)
    return readers, writers


_Monitored = namedtuple('Monitored', 'fp,wants_read,wants_write,callback')
_Event     = namedtuple('Event', 'monitored,readable,writable,fp,callback,ready')


class Monitored(_Monitored):
    """
    Represents the interests of a file handle *fp*,
    and whether it *wants_read* and or *wants_write*,
    as well as an attached *callback*.
    """
    __slots__ = ()


class Event(_Event):
    """
    Represents the readability or writability
    of a *monitored* file object.
    """
    __slots__ = ()

    def __new__(cls, monitored, readable, writable):
        ready = (
            readable >= monitored.wants_read and
            writable >= monitored.wants_write
        )
        return super(Event, cls).__new__(
            cls,
            monitored,
            readable,
            writable,
            fp=monitored.fp,
            callback=monitored.callback,
            ready=ready,
        )
