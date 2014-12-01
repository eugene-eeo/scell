Plugs
=====

Plugs is a simple library for Python that provides a
stateful wrapper around the ``select.select`` function
which allows you to use it easily. It is inspired by
the Ruby nio4r_ library, and similarly can be used as
the heart of *reactor*-based event loops, or implement
evented servers.

Goals of the project include:

 - Expose a high-level API for selectors.
 - Keep the API tiny and try to maximise performance.
 - Make the API sane and elegant

Example Usage:

.. code-block:: python

    from plugs import Plug
    selector = Plug()

    fps = [open(path) for path in PATHS]
    for item in fps:
        mon = selector.register(item, mode='r')
        mon.callback = item.read

    for monitor in selector.select():
        monitor.callback()
        assert not monitor.fp.read()

Plugs is **MIT Licensed**. Do whatever you want with
the codebase, see *LICENSE* for details.
