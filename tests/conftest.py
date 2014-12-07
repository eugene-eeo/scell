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
def handles(request, handle, tmpdir):
    path = tmpdir.join('file2')
    path.write('')

    fp = open(str(path), mode='r+')
    return [handle, fp]


@fixture
def selector(request, handles):
    sel = Selector()
    for item in handles:
        sel.register(item, mode='rw')
    return sel
