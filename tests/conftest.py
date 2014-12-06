from pytest import fixture
from scell import Selector


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
