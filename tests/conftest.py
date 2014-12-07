from pytest import fixture
from scell import Selector


@fixture(params=['w', 'r', 'rw'])
def mode(request):
    return request.param


@fixture
def handle(request, tmpdir):
    fp = tmpdir.join('file')
    fp.write('')
    return open(str(fp), mode='r+')


@fixture
def handles(request, tmpdir):
    paths = [
        tmpdir.join('file.txt'),
        tmpdir.join('open.txt'),
    ]
    for item in paths:
        item.write('')
    return [open(str(p), mode='r+') for p in paths]


@fixture
def selector(request, handles):
    sel = Selector()
    for item in handles:
        sel.register(item, mode='rw')
    return sel
