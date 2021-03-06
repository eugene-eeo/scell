"""
    scell.selector
    ~~~~~~~~~~~~~~

    Implements the ``Selector`` class, a high level
    wrapper around ``~select.select``.
"""


from sys import version_info
from contextlib import contextmanager
from scell.core import select, Monitored, Event

_IS_PY3 = version_info[0] == 3


class Selector(dict):
    """
    A selector object is a dictionary of file-like
    objects to ``Monitored`` objects.
    """

    def register(self, fp, mode, callback=None):
        """
        Register a given *fp* (file handle) under a
        given *mode*. The *mode* can either be ``r``,
        ``w``, or both. Returns the monitor object.

        :param fp: The file-like object.
        :param mode: Whether read and or write-ready
            events should be notified.
        :param callback: Optionally, attach a callback.
        """
        monitor = Monitored(
            fp=fp,
            wants_read='r' in mode,
            wants_write='w' in mode,
            callback=callback,
            )
        self[fp] = monitor
        return monitor

    info = dict.get
    unregister = dict.__delitem__
    registered = property(dict.items if _IS_PY3 else
                          dict.iteritems)

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
        Returns an iterable of monitors which are readable
        or writable subject to *timeout*.

        :param timeout: Maximum number of seconds to
            wait until at least 1 file object is readable or
            writable. To block for an indefinite time, use
            ``None``.
        """
        rl, wl = select(*self.rwlist(), timeout=timeout)
        rl, wl = set(rl), set(wl)

        for fp in rl.union(wl):
            r_ok = fp in rl
            w_ok = fp in wl

            yield Event(monitored=self[fp],
                        readable=r_ok,
                        writable=w_ok)

    def ready(self):
        """
        Yields the registered monitors which are ready
        (their interests are satisfied).
        """
        for event in self.select():
            if event.ready:
                yield event

    @contextmanager
    def scoped(self, fps, mode='rw'):
        """
        A context manager that automatically unregisters
        **fps** once the block has finished executing.

        :param fps: Iterable of file objects.
        :param mode: Defaults to 'rw', the interests of
            every file handle.
        """
        monitors = tuple(self.register(fp, mode) for fp in fps)
        try:
            yield monitors
        finally:
            for mon in monitors:
                if mon.fp in self:
                    self.unregister(mon.fp)
