"""
    scell.wrapper
    ~~~~~~~~~~~~~

    Implements the ``Selector`` class, a high level
    wrapper around ``~select.select``.
"""


from scell.core import select, Monitored


class Selector(object):
    """
    A selector object maintains a dictionary of
    file-like objects to ``~scell.core.Monitored``
    objects.
    """

    def __init__(self):
        self.fps = {}

    def register(self, fp, mode):
        """
        Register a given *fp* (file handle) under a
        given *mode*. The *mode* can either be ``r``,
        ``w``, or both. Returns the monitor object.

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
        file handles to monitor objects.

        :param fp: The file-like object.
        """
        del self.fps[fp]

    def info(self, fp):
        """
        Returns the monitor object for a registered
        file-like object *fp*.

        :param fp: A file-like object that was already
            registered.
        """
        return self.fps[fp]

    @property
    def registered(self):
        """
        Returns an iterable of file-object to monitor
        pairs that are registered on the current
        Selector object.
        """
        for fp in self.fps:
            yield fp, self.fps[fp]

    @property
    def rlist(self):
        """
        Returns a list of file-like objects which are
        interested in readability.
        """
        return [fp for fp, m in self.registered if m.wants_read]

    @property
    def wlist(self):
        """
        Returns a list of file-like objects which are
        interested in writability.
        """
        return [fp for fp, m in self.registered if m.wants_write]

    def select(self, timeout=None):
        """
        Performs a ``~select.select`` call and waits
        for *timeout* seconds, or blocks (forever) if
        *timeout* is not specified. Returns a list of
        readable/writable monitors.

        :param timeout: Maximum number of seconds to
            wait. To block for an indefinite time, use
            ``None`` or to select the monitors which
            are ready, use ``0``.
        """
        rl, wl = select(self.rlist, self.wlist, timeout)
        rl, wl = set(rl), set(wl)
        result = []

        for fp, mon in self.registered:
            mon.readable = fp in rl
            mon.writable = fp in wl

            if mon.readable or mon.writable:
                result.append(mon)

        return result