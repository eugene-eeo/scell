from pytest import raises


def test_select(selector):
    for monitor in selector.select():
        assert monitor.ready


def test_rlist_wlist(selector):
    rlist = set(selector.rlist)
    wlist = set(selector.wlist)

    assert rlist == wlist


def test_only(selector):
    mlist = [m for _, m in selector.registered]

    for mode in ['r', 'w']:
        sel = selector.only(mode)
        res = sel.select()

        assert all(m.ready for m in res)
        assert all(m.ready for m in mlist)

        for m in res:
            m.readable = False
            m.writable = False


def test_unregister(selector):
    for item in selector.rlist:
        selector.unregister(item)

    assert not selector.rlist
    assert not selector.wlist


def test_info(selector):
    rlist = selector.rlist
    for fp in rlist:
        assert selector.info(fp).wants_read
