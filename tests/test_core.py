from itertools import chain
from pytest import mark
from scell.core import select, Monitored


def test_select(handles):
    assert select([], []) == ([], [])
    assert select(handles, []) == (handles, [])
    assert select(handles, handles) == (handles, handles)


def test_monitored(handles, mode):
    for monitor in [Monitored(fp, mode) for fp in handles]:
        assert monitor.mode == mode
        assert not monitor.callback()


@mark.parametrize(
    'fmode,attrs',
    chain(
        [mark.xfail(('rw', m)) for m in [(0,1), (1,0), (0,0)]],
        [('w', m) for m in [(0,1), (1,1)]],
        [('r', m) for m in [(1,0), (1,1)]],
        [('rw', (1,1))],
    )
)
def test_monitored_ready(handles, fmode, attrs):
    for monitor in [Monitored(fp, fmode) for fp in handles]:
        r, w = attrs
        monitor.readable = r
        monitor.writable = w

        assert monitor.ready
        assert monitor.mode == fmode
