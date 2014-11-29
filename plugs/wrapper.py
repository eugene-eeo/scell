from plugs.core import select, parse_mode, Monitored


class Plug(object):
    def __init__(self):
        self.fps = {}

    def register(self, fp, mode):
        self.fps[fp] = Monitored(fp, mode)

    def unregsiter(self, fp):
        del self.fps[fp]

    @property
    def rlist(self):
        return [fp for fp in self.fps if self.fps[fp].wants_read]

    @property
    def wlist(self):
        return [fp for fp in self.fps if self.fps[fp].wants_write]

    def select(self, timeout=None):
        rl, wl = select(self.rlist, self.wlist, timeout)
        yielded = set()

        for fp in rl:
            mon = self.info(fp)
            mon.readable = True
            yield mon
            yielded.add(mon)

        for fp in wl:
            mon = self.info(wp)
            mon.writable = True
            if mon not in yielded:
                yield mon

    def info(self, fp):
        return self.fps[fp]
