from sys import stdout, stderr
from scell import Selector
from pytest import fixture
import scell.core


@fixture(autouse=True)
def mock_select(monkeypatch):
    def select(rlist, wlist, xlist, timeout=None):
        if not timeout and not rlist and not wlist:
            raise RuntimeError
        return rlist, wlist, xlist

    monkeypatch.setattr(scell.core, '_select', select)


@fixture
def handles(request):
    return [stdout, stderr]


@fixture
def selector(request, handles):
    sel = Selector()
    for fp in handles:
        sel.register(fp, mode='rw', callback=lambda: 1)
    return sel
