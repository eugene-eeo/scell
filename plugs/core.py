from select import select as _select
from collections import namedtuple


SelectResult = namedtuple('SelectResult', ('readers', 'writers'))
SelectInfo = namedtuple('SelectInfo', ('obj', 'read', 'write'))


def mode_of(info):
    return ''.join((
        'r' if info.read else '',
        'w' if info.write else '',
    ))


def select(rl, wl):
    r, w, _ = _select(rl, wl, ())
    return SelectResult(r, w)


def parse(mode):
    return 'r' in mode, 'w' in mode
