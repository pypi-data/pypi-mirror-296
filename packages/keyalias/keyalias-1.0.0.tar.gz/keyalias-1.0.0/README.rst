========
keyalias
========

Overview
--------

Add a property that is an alias for an indexer to a class.

Installation
------------

To install ``keyalias``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install keyalias

Implementation
--------------

.. code-block:: python

    import functools
    from tofunc import tofunc

    __all__ = ["keyalias"]

    def keyalias(**kwargs):
        return functools.partial(decorator, **kwargs)

    def propertyget(self, /, *, key):
        return self[key]
    def propertyset(self, value, /, *, key):
        self[key] = value
    def propertydel(self, /, *, key):
        del self[key]
    def decorator(cls, /, **kwargs):
        raws = [propertyget, propertyset, propertydel]
        for alias, key in kwargs.items():
            bindings = list()
            for raw in raws:
                b = functools.partial(raw, key=key)
                b = tofunc(b)
                bindings.append(b)
            pro = property(*bindings)
            setattr(cls, alias, pro)
        return cls

Example
-------

.. code-block:: python

    from keyalias import keyalias

    @keyalias(six=6)
    class MyClass:
        def __init__(self):
            self.data = list(range(10))  # Example list with 10 elements

        def __getitem__(self, index):
            return self.data[index]

        def __setitem__(self, index, value):
            self.data[index] = value

        def __delitem__(self, index):
            del self.data[index]

    # Create an instance of MyClass
    my_instance = MyClass()

    # Use the alias property to access index 6
    print(my_instance.six)  # prints 6
    my_instance.six = 42
    print(my_instance.six)  # prints 42
    del my_instance.six
    print(my_instance.six)  # prints 7

License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/keyalias>`_
* `Download <https://pypi.org/project/keyalias/#files>`_
* `Source <https://github.com/johannes-programming/keyalias>`_

Credits
-------

* Author: Johannes
* Email: `johannes-programming@mailfence.com <mailto:johannes-programming@mailfence.com>`_

Thank you for using ``keyalias``!