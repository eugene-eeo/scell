from pytest import mark
from scell.core import select, Monitored


def test_select(handles):
    assert select([], []) == ([], [])
    assert select(handles, []) == (handles, [])
    assert select(handles, handles) == (handles, handles)


def test_monitored_default_callback():
    monitor = Monitored(None, None, None)
    assert monitor.callback() is None
