from pytest import mark, fixture
from itertools import chain, permutations
from scell.core import select, Monitored


def test_select(handles):
    assert select([], []) == ([], [])
    assert select(handles, []) == (handles, [])
    assert select(handles, handles) == (handles, handles)


def test_monitored(handle, mode):
    monitor = Monitored(handle, mode)
    assert monitor.mode == mode
    assert not monitor.callback()


@mark.parametrize(
    'fmode,passing',
    [
        ('r', [(1, 0), (1, 1)]),
        ('w', [(0, 1), (1, 1)]),
        ('rw', [(1, 1)]),
    ]
)
def test_monitored_ready(handle, fmode, passing):
    monitor = Monitored(handle, fmode)
    for r, w in permutations((0,1)):
        monitor.readable = r
        monitor.writable = w

        if (r, w) in passing:
            assert monitor.ready
        else:
            assert not monitor.ready
