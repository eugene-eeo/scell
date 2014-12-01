Plugs
=====

Plugs is a simple library for Python that provides a
stateful wrapper around the select.select_ function
which allows you to use it easily. It is inspired by
the Ruby nio4r_ library, and similarly can be used as
the heart of *reactor*-based event loops, or implement
evented servers.

Goals of the project include:

* Expose a high-level API for selectors.
* Keep the API tiny and try to maximise performance.
* Make the API sane and elegant


.. _nio4r: https://github.com/celluloid/nio4r
.. _select.select: https://docs.python.org/3/library/select.html#select.select


Usage
-----

.. code-block:: python

    from plugs import Plug
    selector = Plug()

    selector.register(open(PATH), mode='r')
    selector.select()

Note that Plugs is **NOT** an event framework. If you
want to use a framework you are much better off with
the excellent gevent_ or twisted_ frameworks. Plugs
just aims to provide a very minimal API on which
implementers can write libraries or frameworks on top
of without having to deal with some of the lower level
details.


.. _gevent: http://gevent.org
.. _twisted: https://twistedmatrix.com/trac/


License
-------

Plugs is **MIT Licensed**. Do whatever you want with
the codebase, see *LICENSE* for details.
