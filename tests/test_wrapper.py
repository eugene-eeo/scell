from contextlib import contextmanager
from scell import Selector
from pytest import raises


def test_select(selector):
    res = list(selector.select())
    assert res
    for event in res:
        assert event.ready


def test_select_empty():
    sel = Selector()
    assert list(sel.select()) == []


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
    ready = list(selector.ready())
    assert ready

    for event in ready:
        assert event.ready


class TestScoped:
    @contextmanager
    def manager(self, handles):
        self.selector = Selector()
        with self.selector.scoped(handles) as r:
            yield r

    def test_peaceful(self, handles):
        with self.manager(handles) as monitors:
            r = list(self.selector.select())
            assert r
            for ev in r:
                assert ev.monitored in monitors
                assert ev.fp in handles
        assert not self.selector

    def test_exception(self, handles):
        with raises(NameError):
            with self.manager(handles) as _:
                raise NameError
        assert not self.selector
