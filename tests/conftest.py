from sys import stdout, stderr
from scell import Selector
from pytest import fixture


@fixture
def possible(request):
    return [(0, 0), (0, 1), (1, 0), (1, 1)]


@fixture(params=['w', 'r', 'rw'])
def mode(request):
    return request.param


@fixture
def handle(request):
    return stdout


@fixture
def handles(request):
    return [stdout, stderr]


@fixture
def selector(request, handles):
    sel = Selector()
    for item in handles:
        sel.register(item, mode='rw')
    return sel
