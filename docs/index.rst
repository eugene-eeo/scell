.. Scell documentation master file, created by
   sphinx-quickstart on Thu Dec 11 19:22:56 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Scell: Selectors for Humans
===========================

|Build| |Downloads|

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


Contents
--------

.. toctree::
   guide
   api

   :maxdepth: 2


.. |Build| image:: http://img.shields.io/travis/eugene-eeo/scell.svg
   :target: https://travis-ci.org/eugene-eeo/scell
.. |Downloads| image:: https://img.shields.io/pypi/dm/scell.svg
   :target: https://pypi.python.org/pypi/scell
