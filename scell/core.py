"""
    scell.core
    ~~~~~~~~~~

    Provides abstractions over lower level APIs and
    file objects and their interests.
"""


from select import select as _select


def select(rl, wl, timeout=0):
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
    and it's results from a ``select`` call.

    :param fp: The file-like object.
    :param mode: Either 'r', 'w' or 'rw', symbolising
        interest in read, write, and both,
        respectively.
    """

    callback = staticmethod(lambda: None)

    def __init__(self, fp, wants_read, wants_write):
        self.fp = fp
        self.wants_read = wants_read
        self.wants_write = wants_write


class Event(object):
    def __init__(self, monitored, readable, writable):
        self.monitored = monitored
        self.readable = readable
        self.writable = writable

        # convenience methods
        self.fp = monitored.fp
        self.callback = monitored.callback

    @property
    def ready(self):
        return (
            self.readable >= self.monitored.wants_read and
            self.writable >= self.monitored.wants_write
        )
