"""
    plugs.wrapper
    ~~~~~~~~~~~~~

    Implements the ``Plug`` class, which is a high
    level wrapper around select.
"""


from plugs.core import select, Monitored


class Plug(object):
    """
    A plug object maintains a dictionary of file-like
    objects to ``~plugs.core.Monitored`` objects.
    """

    def __init__(self):
        self.fps = {}

    def register(self, fp, mode):
        """
        Register a given *fp* (file handle) under a
        given *mode*. The *mode* can either be ``r``,
        ``w``, or both.

        :param fp: The file-like object.
        :param mode: Whether read and or write-ready
            events should be notified.
        """
        monitor = Monitored(fp, mode)
        self.fps[fp] = monitor
        return monitor

    def unregister(self, fp):
        """
        Removes *fp* from the internal dictionary of
        file handles to ``~plugs.core.Monitored``
        objects.

        :param fp: The file-like object.
        """
        del self.fps[fp]

    @property
    def rlist(self):
        """
        Returns a list of file-like objects which are
        interested in readability.
        """
        return [fp for fp, m in self.fps.items() if m.wants_read]

    @property
    def wlist(self):
        """
        Returns a list of file-like objects which are
        interested in writability.
        """
        return [fp for fp, m in self.fps.items() if m.wants_write]

    def select(self, timeout=None):
        """
        Performs a ``~select.select`` call and waits
        for *timeout* seconds, or blocks (forever) if
        *timeout* is not specified. Yields monitored
        objects to the caller.

        :param timeout: Maximum number of seconds to
            wait. It can be any value but to block for
            an indefinite time, use ``None`` or
            for immediate, use ``0``.
        """
        rl, wl = select(self.rlist, self.wlist, timeout)
        rl, wl = set(rl), set(wl)

        for fp in (rl ^ wl):
            r = fp in rl
            w = fp in wl
            if r or w:
                mon = self.info(fp)
                mon.readable = r
                mon.writable = w
                yield mon

    def info(self, fp):
        """
        Get the ``~plugs.core.Monitored`` object for
        a given file-like object *fp*.

        :param fp: A file-like object that was already
            registered.
        """
        return self.fps[fp]
