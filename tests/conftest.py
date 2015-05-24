from sys import stdout, stderr
from scell import Selector
from pytest import fixture
import scell.core


@fixture(autouse=True)
def mock_select(monkeypatch):
    def select(rlist, wlist, xlist, timeout=None):
        return rlist, wlist, xlist

    monkeypatch.setattr(scell.core, '_select', select)


@fixture
def handle(request):
    return stdout


@fixture
def handles(request):
    return [stdout, stderr]


@fixture
def selector(request, handles):
    sel = Selector()
    for fp in handles:
        sel.register(fp, mode='rw', callback=lambda: 1)
    return sel
