from pytest import fixture
from scell.wrapper import Selector


@fixture
def selector(request, tmpdir):
    paths = [
        tmpdir.join('hello.txt'),
        tmpdir.join('jello.txt'),
    ]
    p = Selector()
    for path in paths:
        path.write('abc')
        p.register(open(str(path), mode='r+'), mode='rw')
    return p


def test_select(selector):
    for monitor in selector.select():
        assert monitor.readable
        assert monitor.wants_read


def test_info(selector):
    for item in selector.rlist:
        assert selector.info(item).wants_read
        assert selector.info(item).mode == 'rw'


def test_ready(selector):
    for item in selector.select():
        assert item.ready()


def test_unregister(selector):
    for item in selector.rlist:
        selector.unregister(item)

    assert not list(selector.select(0))
    assert not list(selector.select())
    assert not selector.rlist


def test_callbacks(selector):
    for mon in selector.values():
        mon.callback = lambda m=mon: m.fp.seek(1)

    for mon in selector.select():
        mon.callback()
        assert mon.fp.tell() == 1


def test_only(selector):
    fps = set(selector.rlist)
    for modestring in ['r', 'w', 'rw']:
        sub = selector.only(modestring)

        assert all(m.readable for m in sub.select())
        assert all(m.readable for fp, m in selector.registered)

        assert set(sub.rlist) == fps
        assert set(sub.wlist) == fps
