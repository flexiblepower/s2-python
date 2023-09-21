Python Wrapper for S2 Flexibility Protocol
===========================================
.. image:: https://img.shields.io/pypi/v/s2-python
   :alt: PyPI - Version
.. image:: https://img.shields.io/pypi/pyversions/s2-python
   :alt: PyPI - Python Version
.. image:: https://img.shields.io/pypi/l/s2-python
   :alt: PyPI - License

This Python package implements the message validation for the EN50491-12-2 "S2" standard for home and building energy management. This implementation
is based on the asyncapi description of the protocol provided in the `s2-ws-json <https://github.com/flexiblepower/s2-ws-json/>`_ repository. 

Currently, the package supports the *common* and *FILL RATE BASED CONTROL* types and messages.

To Install
-----------
You can install this package using pip or any Python dependency manager that collects the packages from Pypi:

.. code-block:: bash

    pip install s2-python

The packages on Pypi may be found `here <https://pypi.org/project/s2-python/>`_

Example
---------

.. code-block:: python

    from s2python.common import PowerRange, CommodityQuantity

    # create s2 messages as Python objects
    number_range = PowerRange(
        start_of_range=4.0,
        end_of_range=5.0,
        commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1,
    )
    # serialize s2 messages
    number_range.to_json()
    # deserialize s2 messages
    json_str = '{"start_of_range": 4.0, "end_of_range": 5.0, "commodity_quantity": "ELECTRIC.POWER.L1"}'
    PowerRange.from_json(json_str)

Development
-------------

For development, you can install the required dependencies using the following command:

    pip install -e .[testing,development]


The tests can be run using tox:

    tox

To build the package, you can use tox as well:

    tox -e build,clean
    


