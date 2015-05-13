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

    readable = 0
    writable = 0
    callback = staticmethod(lambda: None)

    def __init__(self, fp, mode):
        self.fp = fp
        self.wants_read = int('r' in mode)
        self.wants_write = int('w' in mode)

    @property
    def mode(self):
        """
        Returns the mode as a string, taking into
        account any changes that might be made on
        the object's interests.
        """
        return ''.join((
            'r' if self.wants_read else '',
            'w' if self.wants_write else '',
            ))

    @property
    def ready(self):
        """
        Tells whether the monitor object is ready
        or not- whether it's readability and
        writability interests are met.
        """
        return (
            self.readable >= self.wants_read and
            self.writable >= self.wants_write
            )
