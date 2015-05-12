"""
    scell.wrapper
    ~~~~~~~~~~~~~

    Implements the ``Selector`` class, a high level
    wrapper around ``~select.select``.
"""


from sys import version_info
from contextlib import contextmanager
from scell.core import select, Monitored


class Selector(dict):
    """
    A selector object is a dictionary of file-like
    objects to ``Monitored`` objects.
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

    info = dict.get
    unregister = dict.__delitem__
    registered = property(dict.items if version_info[0] == 3 else
                          dict.iteritems)

    @property
    def rwlist(self):
        """
        Returns ``(rl, wl)`` where ``rl`` and ``wl``
        are file objects interested in readability
        and writability, respectively.
        """
        rl, wl = [], []
        for fp, mon in self.registered:
            if mon.wants_read:
                rl.append(fp)
            if mon.wants_write:
                wl.append(fp)
        return rl, wl

    def select(self, timeout=None):
        """
        Returns a list of monitors which are readable
        or writable, i.e. their readability/writability
        has changed, subject to *timeout*.

        :param timeout: Maximum number of seconds to
            wait. To block for an indefinite time, use
            ``None`` or to select the monitors which
            are ready, use ``0``.
        """
        rl, wl = select(*self.rwlist, timeout=timeout)
        rl, wl = set(rl), set(wl)
        result = []

        for fp, mon in self.registered:
            r_ok = mon.readable = fp in rl
            w_ok = mon.writable = fp in wl

            if r_ok or w_ok:
                result.append(mon)

        return result

    @property
    def ready(self):
        """
        Yields the registered monitors which are ready
        (their interests are satisfied).
        """
        for fp, mon in self.registered:
            if mon.ready:
                yield mon

    @contextmanager
    def scoped(self, fps, mode='rw'):
        """
        A context manager that automatically unregisters
        **fps** once the block has finished executing.

        :param fps: Iterable of file objects.
        :param mode: Defaults to 'rw', the interests of
            every file handle.
        """
        monitors = [self.register(fp, mode) for fp in fps]
        try:
            yield monitors
        finally:
            for mon in monitors:
                if mon.fp not in self:
                    continue
                self.unregister(mon.fp)
