from sys import stdout, stderr
from scell import Selector
from pytest import fixture


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
