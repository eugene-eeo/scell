Plugs: Selectors for Humans
===========================

Plugs is a MIT-licensed selector library, written in Python.

At the heart of event-driven platforms is the selector, the
humble **select.select** function. Using it is very simple,
but requires you to pass in lists of file handles again and
again. Keeping track of these file handles are tricky. Let
Plugs handle it for you and you can focus on building an
awesome library/server.::

    >>> selector = plugs.Plug()
    >>> monitor = selector.register(open('file.txt'), mode='r')
    >>> monitor.callback = lambda: 1
    >>> r = selector.select()
    >>> monitor.readable
    True
    >>> [m.callback() for m in r]
    [1]

Plugs allows implementors to effortlessly build libraries
atop of the minimal abstraction provided, while also having
good performance. The API is very small and works across
many platforms, including Windows and OSX.

Features
--------

- Stateful wrapper around **select.select**
- Extremely small API with small footprint
- Efficient implementation of callbacks
- Core abstractions can be used directly
