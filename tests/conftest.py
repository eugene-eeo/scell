import platform
from sys import stdout, stderr
from scell import Selector
from pytest import fixture


PLATFORM = platform.system().lower()


if 'win' in PLATFORM or 'nt' in PLATFORM:
    @fixture(autouse=True)
    def select_no_io(monkeypatch):
        monkeypatch.setattr(
            'select.select',
            lambda rl, wl, xl, timeout=None: (rl, wl, xl),
        )


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
        sel.register(fp, mode='rw')
    return sel
