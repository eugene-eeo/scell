from plugs.core import SelectInfo, mode_of, select, parse


class Plug(object):
    def __init__(self):
        self.rlist = []
        self.wlist = []

    def register(self, fp, mode='r'):
        for item in self.parse(mode):
            item.append(fp)

    def remove(self, fp, mode=None):
        for item in self.parse(mode or mode_of(self.info(fp))):
            item.remove(fp)

    def wait(self):
        return select(self.rlist, self.wlist)

    def info(self, fp):
        return SelectInfo(
            obj=fp,
            read=fp in self.rlist,
            write=fp in self.wlist,
        )

    def parse(self, mode):
        read, write = parse(mode)
        if read:
            yield self.rlist
        if write:
            yield self.wlist
