from scell.core import select, Monitored


def test_select(handles):
    assert select([], []) == ([], [])
    assert select(handles, []) == (handles, [])
    assert select(handles, handles) == (handles, handles)


def test_monitored(handles):
    for monitor in [Monitored(fp, 'rw') for fp in handles]:
        monitor.readable = True
        monitor.writable = True

        assert monitor.mode == 'rw'
        assert monitor.ready
        assert not monitor.callback()
