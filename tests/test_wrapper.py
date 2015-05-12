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


def test_only(selector, mode):
    mlist = [m for _, m in selector.registered]
    sel = selector.only(mode)
    res = sel.select()

    assert all(m.ready for m in res)
    assert all(m.ready for m in mlist)


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


def test_monitors(handles):
    s = Selector()
    with s.monitors(handles) as (m1,m2):
        s.select()
        assert m1.ready
        assert m2.ready
    assert not s


def test_monitors_exception(handles):
    s = Selector()
    with raises(NameError):
        with s.monitors(handles) as _:
            raise NameError
    assert not s
