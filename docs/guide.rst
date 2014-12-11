Guide
=====

Scell is a very simple library that is comprised of two
main components- the core library, which implements
wrappers around monitored file objects and the :func:`select.select`
function, and the wrapper which implements a :class:`scell.wrapper.Selector`
object atop a dictionary.


Registering File Objects
------------------------

To instantiate the **Selector** object just call the
class without any arguments. You can then register
file objects onto the instance::

    >>> from scell import Selector
    >>> selector = Selector()
    >>> mon = selector.register(open('file.txt'), mode='r')

A :class:`scell.core.Monitored` object will be returned,
which represents a registered (monitored) file object,
and it's interests and readiness. For example if you want
to check if a monitored object is readable or writable,
and whether it is interested in readability and writability
you can do::

    >>> mon.readable
    False
    >>> mon.writable
    False
    >>> mon.wants_read
    True
    >>> mon.wants_write
    False

With those four attributes, you can judge whether a
monitored object is *ready* by comparison. Alternatively
you can use the calculated, dynamic properties::

    >>> mon.ready
    False
    >>> mon.mode
    'r'

Iteration
#########

You can get an iterable of file object and monitored
objects with the :attr:`scell.wrapper.Selector.registered`
property::

    for fp, mon in selector.registered:
        # do something

.. WARNING::
   You cannot modify the selector object (which is
   a dictionary subclass) while iterating over the
   ``registered`` property.

Alternatively if you want to only get the keys in a
consistent (Python 2.x and 3.x) and modification resistant
way (you can modify the selector while iterating), use
the ``handles`` attribute, for example::

    for fp in selector.handles:
        # do something

Getting Monitored Objects
#########################

It is not practical for the user code to be in charge of
keeping the monitored objects around without any way of
querying for the same registered object. To do that use
the :meth:`scell.wrapper.Selector.info` method::

    selector.info(fp)


Waiting for IO Events
---------------------

Call the :meth:`scell.wrapper.Selector.select` method on
the selector object to get a list of monitored objects
which are ready for either read or write (though they may
not necessarily be *ready*, that is that their interests
may not be fulfilled)::

    >>> selector.select()
    [<scell.core.Monitored object at 0x...>]

You can also pass a value to the method to specify the
timeout. For example, to select the file objects which
are immediately ready, use ``0``, to block for an
indefinite time use ``None``::

    selector.select(0)
    selector.select(None)

To get a list of monitored objects which are *ready*,
use the :attr:`scell.wrapper.Selector.ready` property,
for example::

    >>> list(selector.ready)
    [<scell.core.Monitored object at 0x...>]

Callbacks
#########

Callbacks can be easily implemented using the ``callback``
attribute of monitored objects. However scell will not
call the callbacks directly. It is up to the user code
to decide when and where to call them::

    for mon in selector.values():
        mon.callback = lambda: 1

    [mon.callback() for mon in selector.ready]


Unregistering File Objects
--------------------------

Once you are done monitoring a file object, you will
typically want to un-register it from the selector
object. To do that use the :meth:`scell.wrapper.Selector.unregister`
method, for example::

    for mon in selector.handles:
        selector.unregister(mon)
