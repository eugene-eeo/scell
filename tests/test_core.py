from pytest import mark, fixture
from scell.core import select, Monitored, Event


def test_select(handles):
    assert select([], []) == ([], [])
    assert select(handles, []) == (handles, [])
    assert select(handles, handles) == (handles, handles)


@fixture
def monitored():
    return Monitored(fp=None,
                     wants_read=True,
                     wants_write=True,
                     callback=None)


def test_monitored_callback(monitored):
    assert monitored.callback is None


@mark.parametrize('changes,ok', [
    ((1,0), False),
    ((0,1), False),
    ((0,0), False),
    ((1,1), True),
])
def test_event_ready(monitored, changes, ok):
    event = Event(monitored, *changes)
    assert event.ready == ok


def test_event_attrs(monitored):
    event = Event(monitored, 1, 1)
    assert event.fp is monitored.fp
    assert event.callback is monitored.callback
