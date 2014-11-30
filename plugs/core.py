"""
    plugs.core
    ~~~~~~~~~~

    Provides abstractions over the lower level APIs.
"""


from select import select as _select


def select(rl, wl, timeout):
    """
    Performs a ``~select.select`` call with the given
    read-list (*rl*), write-list (*wl*), and *timeout*
    in seconds.

    :param rl: Objects interested in readability.
    :param wl: Objects interested in writability.
    :param timeout: Maximum blocking time in seconds.
    """
    if not (rl or wl):
        return [], []
    rlist, wlist, _ = _select(rl, wl, (), timeout)
    return rlist, wlist


class Monitored(object):
    """
    Represents the interests of a file handle, and
    it's results from a ``~plugs.core.select`` call.

    :param fp: The file-like object.
    :param mode: Either 'r', 'w' or 'rw', symbolising
        interest in read, write, and both,
        respectively.
    """

    readable = False
    writable = False

    def __init__(self, fp, mode):
        self.fp = fp
        self.wants_read = 'r' in mode
        self.wants_write = 'w' in mode

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

    @staticmethod
    def callback():
        """
        A static method that can be overriden to
        effectively implement callbacks that can
        be triggered after the object is ready.
        """
        return
