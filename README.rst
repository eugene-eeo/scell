Scell: Selectors for Humans
===========================

|Build| |Version|

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
    >>> ready = selector.select()
    >>> monitor.readable
    True
    >>> [m.callback() for m in ready]
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
- Highly documented codebase


Installation
------------

To install Scell, simply::

    $ pip install scell

.. |Build| image:: http://img.shields.io/travis/eugene-eeo/scell.svg
   :target: https://travis-ci.org/eugene-eeo/scell
.. |Version| image:: http://img.shields.io/pypi/v/scell.svg
   :target: https://pypi.python.org/pypi/scell
