from plugs.core import Monitored, select


def test_select(tmpdir):
    handles = []
    paths = [tmpdir.join(p) for p in ['h', 'g']]

    for item in paths:
        item.write('')
        handles.append(open(str(item)))

    assert select(handles, [], 0) == (handles, [])
    assert select([], [], 0) == ([], [])


def test_monitored():
    m = Monitored(None, 'rw')

    assert m.wants_read
    assert m.wants_write
    assert m.mode == 'rw'

    assert not m.readable
    assert not m.writable

    m.wants_read = False
    assert m.mode == 'w'

    m.callback()
