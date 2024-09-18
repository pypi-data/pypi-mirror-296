======
tofunc
======

Overview
--------

Convert any callable into a function. Useful to circumvent method binding.

Installation
------------

To install ``tofunc``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install tofunc

Implementation
--------------

.. code-block:: python

    import functools

    __all__ = ["tofunc"]

    def tofunc(old, /):
        def new(*args, **kwargs):
            return old(*args, **kwargs)
        try:
            new = functools.wraps(old)(new)
        except:
            pass
        return new

Example
-------

.. code-block:: python

    from tofunc import tofunc
    import functools

    def join(self, b="beta", c="gamma"):
        return "%s %s %s" % (self, b, c)

    hello = functools.partial(join, c="hello")
    class Foo:
        ...
    Foo.greet = hello
    print(Foo().greet("Alice"))
    # Output: Alice beta hello
    hello = tofunc(hello)
    Foo.greet = hello
    print(Foo().greet("Bob"))
    # Output: <__main__.Foo object at 0x1443bfce0> Bob hello

License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/tofunc>`_
* `Download <https://pypi.org/project/tofunc/#files>`_
* `Source <https://github.com/johannes-programming/tofunc>`_

Credits
-------

* Author: Johannes
* Email: `johannes-programming@mailfence.com <mailto:johannes-programming@mailfence.com>`_

Thank you for using ``tofunc``!