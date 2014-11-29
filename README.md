plugs
=====

Plugs is a wrapper around the ``select.select`` API in Python
that provides an object which IO objects can be registered
onto. It is inspired by **nio4r** Example usage:

```python
from plugs import Plug
plug = Plug()

plug.register(conn, mode='rw')
plug.register(fp, mode='r')
```
