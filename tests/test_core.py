from pytest import mark
from scell.core import select, Monitored


def test_select(handles):
    assert select([], []) == ([], [])
    assert select(handles, []) == (handles, [])
    assert select(handles, handles) == (handles, handles)


def test_monitored(handle, mode):
    monitor = Monitored(handle, mode)
    assert monitor.mode == mode
    assert monitor.callback() is None


@mark.parametrize('fmode,ok', [
    ('r', (1, 0)),
    ('w', (0, 1)),
    ('rw', (1, 1)),
])
def test_monitored_mode(handle, fmode, ok, possible):
    monitor = Monitored(handle, '')

    for r, w in possible:
        monitor.wants_read = r
        monitor.wants_write = w

        if (r, w) == ok:
            assert monitor.mode == fmode
            continue

        assert monitor.mode != fmode


@mark.parametrize('fmode,ok', [
    ('r', [(1, 0), (1, 1)]),
    ('w', [(0, 1), (1, 1)]),
    ('rw', [(1, 1)]),
])
def test_monitored_ready(handle, fmode, ok, possible):
    monitor = Monitored(handle, fmode)

    for r, w in possible:
        monitor.readable = r
        monitor.writable = w

        if (r, w) in ok:
            assert monitor.ready
            continue

        assert not monitor.ready
