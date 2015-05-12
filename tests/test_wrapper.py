from contextlib import contextmanager
from scell import Selector
from pytest import raises


def test_select(selector):
    res = selector.select()
    assert res
    for monitor in res:
        assert monitor.ready


def test_select_empty():
    sel = Selector()
    assert sel.select() == []


def test_unregister(selector):
    for fp in list(selector):
        selector.unregister(fp)
    assert not selector


def test_info(selector):
    for fp in selector:
        assert selector.info(fp).wants_read

    assert selector.info(0) is None


def test_callbacks(selector):
    for _, mon in selector.registered:
        mon.callback = lambda: 1
    res = selector.select()
    exp = len(selector)
    assert sum(m.callback() for m in res) == exp


def test_ready(selector):
    results = selector.select()
    ready = list(selector.ready)

    assert ready
    assert len(ready) == len(selector)

    for monitor in ready:
        assert monitor.ready
        assert monitor in results


class TestScoped:
    @contextmanager
    def manager(self, handles):
        s = Selector()
        with s.scoped(handles) as r:
            yield s, r

    def test_peaceful(self, handles):
        with self.manager(handles) as (s, (m1,m2)):
            s.select()
            assert m1.ready
            assert m2.ready
        assert not s

    def test_exception(self, handles):
        with raises(NameError):
            with self.manager(handles) as (s, _):
                raise NameError
        assert not s
