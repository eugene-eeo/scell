Guide
=====

Scell is a very simple library that is comprised of two
main components- the core library, which implements
wrappers around monitored file objects and the :func:`select.select`
function, and the wrapper which implements a :class:`scell.wrapper.Selector`
object atop a dictionary. To get started with the rest
of the guide first create a :class:`scell.wrapper.Selector`
instance:

.. code-block:: python

    selector = Selector()


Registering File Objects
------------------------

The recommended way to register file objects for their
interests is using the :func:`scell.wrapper.Selector.scoped`
context manager:

.. code-block:: python

    with selector.scoped([fp1, fp2]) as (m1, m2):
        pass

Within the body of the ``with`` block, the file objects
are registered but once the block exits the selector
automatically unregisters them. This ensures that file
objects are automatically cleaned up and that unneeded
resources can be freed. You can also use the alternative
forms:

.. code-block:: python

    # more verbose but more control
    from scell.core import Monitored
    selector[fp] = Monitored(
        fp,
        wants_read=True,
        wants_write=True,
        callback=None,
    )

    # easier but less control
    selector.register(fp, mode='rw', callback=None)

You can also attach callbacks or other form of data
alongside the registered file object:

.. code-block:: python

    monitor = selector.register(fp, mode='rw')
    monitor.callback = lambda x: x


Querying Events
---------------

You can query for readability or writability of each
file object by simply using the :func:`scell.wrapper.Selector.select`
method:

.. code-block:: python

    for event in selector.select():
        assert event.readable
        assert event.writable

The ``select`` method returns an iterable of :class:`scell.core.Event`
objects that represents the readability and writability
of the monitored file objects. A code example of the
attributes and what they are:

.. code-block:: python

    event.readable     # whether the file object is readable
    event.writable     # whether the file object is writable
    event.ready        # whether the monitored meets are met
    event.fp           # underlying file object
    event.callback     # callback associated with the file object
    event.monitored    # monitored interests of file object

To only select file objects which are ready, use the
:func:`scell.wrapper.Selector.ready` method. For example:

.. code-block:: python

    for event in selector.ready():
        assert event.ready


Cleaning Up
-----------

Cleaning up after ourselves is important- that is, to
unregister file objects that have already been closed
or unregister file objects that we are no longer
interested in. If you used the :func:`scell.wrapper.Selector.scoped`
you don't need to unregister any file objects.

To unregister file objects use the :func:`scell.wrapper.Selector.unregister`
method:

.. code-block:: python

    selector.unregister(fp)

Note that it raises a ``KeyError`` if you unregister
file objects that are not present.
