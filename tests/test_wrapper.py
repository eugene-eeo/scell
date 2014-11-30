from pytest import fixture
from plugs.wrapper import Plug


@fixture
def plug(request, tmpdir):
    paths = [
        tmpdir.join('hello.txt'),
        tmpdir.join('jello.txt'),
    ]
    p = Plug()
    for path in paths:
        path.write('')
        p.register(open(str(path)), mode='r')
    return p


def test_select(plug):
    for monitor in plug.select():
        assert monitor.readable
        assert monitor.wants_read


def test_info(plug):
    for item in plug.rlist:
        assert plug.info(item).wants_read
        assert plug.info(item).mode == 'r'


def test_unregister(plug):
    for item in plug.rlist:
        plug.unregister(item)

    assert not list(plug.select(0))
    assert not plug.rlist
