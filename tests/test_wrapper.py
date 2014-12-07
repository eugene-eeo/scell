from pytest import raises


def test_select(selector):
    for monitor in selector.select():
        assert monitor.ready


def test_rlist_wlist(selector):
    rlist = set(selector.rlist)
    wlist = set(selector.wlist)

    assert rlist == wlist


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
