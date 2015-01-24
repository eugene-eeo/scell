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
    def handles(self):
        """
        Returns a list of registered file objects,
        ideal for use where you might modify the
        selector while iterating.
        """
        return [fp for fp in self]

    @property
    def rwlist(self):
        """
        Returns a tuple of lists of file objects that
        are interested in readability and writability,
        respectively.
        """
        rl, wl = [], []
        for fp, mon in self.registered:
            if mon.wants_read:
                rl.append(fp)
            if mon.wants_write:
                wl.append(fp)
        return rl, wl

    def only(self, mode):
        """
        Returns a new selector object with only the
        monitors which are interested in a given *mode*,
        i.e. if ``mode='r'`` monitors with 'rw' or 'r'
        will be registered on the new selector.

        :param mode: Desired mode.
        """
        selector = Selector()
        for fp, mon in self.registered:
            if mode in mon.mode:
                selector[fp] = mon
        return selector

    def select(self, timeout=None):
        """
        Returns a list of monitors which are readable
        or writable.

        :param timeout: Maximum number of seconds to
            wait. To block for an indefinite time, use
            ``None`` or to select the monitors which
            are ready, use ``0``.
        """
        rl, wl = select(*self.rwlist, timeout=timeout)
        rl, wl = set(rl), set(wl)
        result = []

        for fp, mon in self.registered:
            mon.readable = fp in rl
            mon.writable = fp in wl

            if mon.readable or mon.writable:
                result.append(mon)

        return result

    @property
    def ready(self):
        """
        Yields the registered monitors which are ready
        (their interests are satisfied).
        """
        return [mon for _, mon in self.registered if mon.ready]
