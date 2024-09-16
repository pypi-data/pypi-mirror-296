======
judson
======

Overview
--------

The ``judson`` project contains the ``judson`` function. This function creates a dictionary from two iterators of the same length using the howe project. The judson project is named for W. L. Judson, one of the inventors of the zipper.

Installation
------------

To install judson, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install judson

Example
-------

.. code-block:: python

    # Import the judson function from the judson package
    from judson import judson

    # Example iterators (can be lists, tuples, or other iterables of the same length)
    keys = ['name', 'age', 'location']
    values = ['Alice', 30, 'New York']

    # Use the judson function to combine them into a dictionary
    result = judson(keys, values)

    # Output the result
    print(result)

    # Output:
        # {'name': 'Alice', 'age': 30, 'location': 'New York'}

License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/judson>`_
* `Download <https://pypi.org/project/judson/#files>`_
* `Source <https://github.com/johannes-programming/judson>`_

Credits
-------
* Author: Johannes
* Email: johannes-programming@mailfence.com

Thank you for using ``judson``!