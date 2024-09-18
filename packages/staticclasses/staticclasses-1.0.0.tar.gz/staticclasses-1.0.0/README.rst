=============
staticclasses
=============

Overview
--------

Create static classes in python.

Installation
------------

To install ``staticclasses``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install staticclasses

Implementation
--------------

.. code-block:: python

    class staticmeta(type):
        def __call__(cls, *args, **kwargs):
            e = "Cannot instantiate static class %r!"
            e %= cls.__name__
            raise TypeError(e)


    class staticclass(metaclass=staticmeta): ...

License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/staticclasses>`_
* `Download <https://pypi.org/project/staticclasses/#files>`_
* `Source <https://github.com/johannes-programming/staticclasses>`_

Credits
-------

* Author: Johannes
* Email: `johannes-programming@mailfence.com <mailto:johannes-programming@mailfence.com>`_

Thank you for using ``staticclasses``!