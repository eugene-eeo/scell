Scell: Selectors for Humans
===========================

|AppVeyor| |Build| |Downloads|

Scell is a MIT-licensed selector library, written in Python.

At the heart of event-driven platforms is the selector, the
humble **select.select** function. Using it is very simple,
but requires you to pass in lists of file handles again and
again. Keeping track of these file handles are tricky. Let
Scell handle it for you and focus on building an awesome
library/server::

    >>> selector = scell.Selector()
    >>> monitor = selector.register(open('file.txt'), mode='r')
    >>> monitor.callback = lambda: 1
    >>> [event.callback() for event in selector.ready]
    [1]

Scell allows implementors to effortlessly build libraries
atop of the minimal abstraction provided, while also having
good performance. The API is very small and works across
many platforms, including Windows and OSX.


Features
--------

- Stateful wrapper around **select.select**
- Extremely small API with small footprint and 100% coverage
- Core abstractions and utilities can be used directly
- Efficient implementation of callbacks
- Highly `documented`_ codebase

.. _documented: https://scell.readthedocs.org


Installation
------------

To install Scell, simply::

    $ pip install scell

.. |AppVeyor| image:: https://ci.appveyor.com/api/projects/status/lk3qglnh5edw05xe?svg=true
   :target: https://ci.appveyor.com/project/eugene-eeo/scell
.. |Build| image:: http://img.shields.io/travis/eugene-eeo/scell.svg
   :target: https://travis-ci.org/eugene-eeo/scell
.. |Downloads| image:: https://img.shields.io/pypi/dm/scell.svg
   :target: https://pypi.python.org/pypi/scell
