from select import select as _select


def select(rl, wl, timeout):
    rlist, wlist, _ = _select(rl, wl, (), timeout)
    return rlist, wlist


class Monitored(object):
    readable = False
    writable = False

    def __init__(self, fp, mode):
        self.fp = fp
        self.wants_read = 'r' in mode
        self.wants_write = 'w' in mode

    @property
    def mode(self):
        return ''.join((
            'r' if self.wants_read else '',
            'w' if self.wants_write else '',
        ))
