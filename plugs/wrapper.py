from plugs.core import select, Monitored


class Plug(object):
    def __init__(self):
        self.fps = {}

    def register(self, fp, mode):
        self.fps[fp] = Monitored(fp, mode)

    def unregister(self, fp):
        del self.fps[fp]

    @property
    def rlist(self):
        return [fp for fp in self.fps if self.fps[fp].wants_read]

    @property
    def wlist(self):
        return [fp for fp in self.fps if self.fps[fp].wants_write]

    def select(self, timeout=None):
        rl, wl = select(self.rlist, self.wlist, timeout)
        rl, wl = set(rl), set(wl)

        for fp in self.fps:
            r = fp in rl
            w = fp in wl
            if r or w:
                mon = self.fps[fp]
                mon.readable = r
                mon.writable = w
                yield mon

    def info(self, fp):
        return self.fps[fp]
