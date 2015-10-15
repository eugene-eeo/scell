from contextlib import contextmanager
from scell import Selector
from pytest import raises, fixture


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
    res = selector.select()
    exp = len(selector)
    assert sum(m.callback() for m in res) == exp


def test_ready(selector):
    ready = list(selector.ready())
    assert ready

    for event in ready:
        assert event.ready


class TestScoped(object):
    @fixture
    def sel(self):
        return Selector()

    def test_peaceful(self, sel, handles):
        with sel.scoped(handles) as monitors:
            r = set(k.fp for k in sel.ready())
            assert r == set(handles)
        assert not sel

    def test_exception(self, sel, handles):
        with raises(NameError):
            with sel.scoped(handles) as _:
                raise NameError
        assert not sel
