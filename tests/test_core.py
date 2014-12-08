from pytest import mark
from itertools import chain, product
from scell.core import select, Monitored


def test_select(handles):
    assert select([], []) == ([], [])
    assert select(handles, []) == (handles, [])
    assert select(handles, handles) == (handles, handles)


def test_monitored(handle, mode):
    monitor = Monitored(handle, mode)
    assert monitor.mode == mode
    assert not monitor.callback()


@mark.parametrize('fmode,ok', [
    ('r', [(1, 0), (1, 1)]),
    ('w', [(0, 1), (1, 1)]),
    ('rw', [(1, 1)]),
])
def test_monitored_ready(handle, fmode, ok):
    monitor = Monitored(handle, fmode)
    for r, w in product((0, 1), repeat=2):
        monitor.readable = r
        monitor.writable = w

        if (r, w) in ok:
            assert monitor.ready
            continue

        assert not monitor.ready
