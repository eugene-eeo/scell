from sys import stdout, stderr
from scell import Selector
from pytest import fixture


@fixture(params=['w', 'r', 'rw'])
def mode(request):
    return request.param


@fixture
def handle(request, tmpdir):
    fp = tmpdir.join('file')
    fp.write('')
    return fp.open(mode='r+')


@fixture(params=['stdio', 'files'])
def handles(request, tmpdir):
    if request.param == 'stdio':
        return [stdout, stderr]

    paths = [tmpdir.join(x) for x in ['file1', 'file2']]
    for item in paths:
        item.write('')
    return [x.open(mode='r+') for x in paths]


@fixture
def selector(request, handles):
    sel = Selector()
    for item in handles:
        sel.register(item, mode='rw')
    return sel
