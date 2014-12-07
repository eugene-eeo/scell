from scell.core import select, Monitored


def test_select(handles):
    assert select([], []) == ([], [])
    assert select(handles, []) == (handles, [])
    assert select(handles, handles) == (handles, handles)


def test_monitored(handles, mode):
    for monitor in [Monitored(fp, mode) for fp in handles]:
        monitor.readable = True
        monitor.writable = True

        assert monitor.mode == mode
        assert monitor.ready
        assert not monitor.callback()
