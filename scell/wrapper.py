"""
    scell.wrapper
    ~~~~~~~~~~~~~

    Implements the ``Selector`` class, a high level
    wrapper around ``~select.select``.
"""


from sys import version_info
from functools import wraps
from scell.core import select, Monitored


def _generate_items(cls, major_version=version_info[0]):
    if major_version == 3:
        return cls.items
    @wraps(cls.items)
    def items(self):
        for item in self:
            yield item, self[item]
    return items


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
    registered = property(_generate_items(dict))

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

    def only(self, mode):
        """
        Returns a new selector object with only monitors
        which are interested in a given *mode*, i.e. if
        ``mode='r'`` monitors with 'rw' or 'r' will be
        registered on the new selector.

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
