"""
    scell.wrapper
    ~~~~~~~~~~~~~

    Implements the ``Selector`` class, a high level
    wrapper around ``~select.select``.
"""


from scell.core import select, Monitored


class Selector(dict):
    """
    A selector object is a dictionary of file-like
    objects to ``~scell.core.Monitored`` objects.
    """

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
        self[fp] = monitor
        return monitor

    info = dict.__getitem__
    unregister = dict.__delitem__

    @property
    def registered(self):
        """
        Returns an iterable of file-like object to
        monitor pairs that are registered on the
        current Selector object.
        """
        for fp in self:
            yield fp, self[fp]

    @property
    def rlist(self):
        """
        Returns a list of file-like objects which are
        interested in readability.
        """
        return [fp for fp in self if self[fp].wants_read]

    @property
    def wlist(self):
        """
        Returns a list of file-like objects which are
        interested in writability.
        """
        return [fp for fp in self if self[fp].wants_write]

    def only(self, mode):
        """
        Returns a new selector object with only the
        monitors which are interested in a given *mode*,
        i.e. if *mode*='r' monitors with 'rw' or 'r'
        will be registered on the new selector.

        :param mode: Whether monitors interested in
            read and or write should be registered.
        """
        selector = Selector()
        for fp, mon in self.registered:
            if mode in mon.mode:
                selector[fp] = mon
        return selector

    def select(self, timeout=None):
        """
        Performs a ``~select.select`` call and waits
        for *timeout* seconds, or blocks (forever) if
        *timeout* is not specified. Returns a list of
        readable and or writable monitors.

        :param timeout: Maximum number of seconds to
            wait. To block for an indefinite time, use
            ``None`` or to select the monitors which
            are ready, use ``0``.
        """
        rl, wl = select(self.rlist, self.wlist, timeout)
        rl, wl = set(rl), set(wl)
        ready = []

        for fp, mon in self.registered:
            mon.readable = fp in rl
            mon.writable = fp in wl

            if mon.readable or mon.writable:
                ready.append(mon)

        return ready

    @property
    def ready(self):
        """
        Yields the registered monitors which can
        be either written to or read from, depending
        on their mode.
        """
        for _, mon in self.registered:
            if mon.ready:
                yield mon
