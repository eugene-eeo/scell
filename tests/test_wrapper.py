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


def test_rlist_wlist(handles, mode):
    sel = Selector()
    for item in handles:
        sel.register(item, mode)

    for char in mode:
        assert getattr(sel, '%slist' % char)


def test_only(selector, mode):
    mlist = [m for _, m in selector.registered]
    sel = selector.only(mode)
    res = sel.select()

    assert all(m.ready for m in res)
    assert all(m.ready for m in mlist)


def test_unregister(selector):
    for item in selector.rlist:
        selector.unregister(item)

    assert not selector.rlist
    assert not selector.wlist


def test_info(selector):
    for fp in selector.rlist:
        assert selector.info(fp).wants_read


def test_info_nonexistent(selector):
    with raises(KeyError):
        selector.info('')


def test_callbacks(selector):
    for _, mon in selector.registered:
        mon.callback = lambda: 1

    res = selector.select()
    assert [m.callback() for m in res] == [1, 1]
