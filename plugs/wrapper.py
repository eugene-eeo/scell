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
        rl, wl = set(rl), set(wl)

        for fp in self.fps:
            item = self.fps[fp]
            if item not in rl and item not in wl:
                continue
            item.readable = fp in rl
            item.writable = fp in wl
            yield item

    def info(self, fp):
        return self.fps[fp]
