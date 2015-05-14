"""
    scell.core
    ~~~~~~~~~~

    Provides abstractions over lower level APIs and
    file objects and their interests.
"""


from select import select as _select


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


class Monitored(object):
    """
    Represents the interests of a file handle *fp*,
    and whether it *wants_read* and or *wants_write*.
    """

    callback = staticmethod(lambda: None)

    def __init__(self, fp, wants_read, wants_write):
        self.fp = fp
        self.wants_read = wants_read
        self.wants_write = wants_write


class Event(object):
    """
    Represents the readability or writability
    of a *monitored* file object.
    """

    def __init__(self, monitored, readable, writable):
        self.monitored = monitored
        self.readable = readable
        self.writable = writable

        # convenience attributes
        self.fp = monitored.fp
        self.callback = monitored.callback

    @property
    def ready(self):
        """
        Whether the *monitored* needs are met,
        i.e. whether it is readable or writable,
        taking it's needs into account.
        """
        return (
            self.readable >= self.monitored.wants_read and
            self.writable >= self.monitored.wants_write
        )
