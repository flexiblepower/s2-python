Python Wrapper for S2 Flexibility Protocol
===========================================
|PyPI pyversions|

.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/ansicolortags.svg
   :target: https://pypi.python.org/pypi/s2-python/

|PyPI version fury.io|

.. |PyPI version fury.io| image:: https://badge.fury.io/py/ansicolortags.svg
   :target: https://pypi.python.org/pypi/s2-python/

|PyPI download total|

.. |PyPI download total| image:: https://img.shields.io/pypi/dt/ansicolortags.svg
   :target: https://pypi.python.org/pypi/s2-python/

|PyPI license|

.. |PyPI license| image:: https://img.shields.io/pypi/l/ansicolortags.svg
   :target: https://pypi.python.org/pypi/s2-python/

This Python package implements the message validation for the EN50491-12-2 "S2" standard for home and building energy management. This implementation
is based on the asyncapi description of the protocol provided in the `s2-ws-json <https://github.com/flexiblepower/s2-ws-json/>`_ repository. 

Currently, the package supports the *common* and *FILL RATE BASED CONTROL* types and messages.


Example
---------
Short code snippet::

.. code-block:: python
        >> number_range = PowerRange(start_of_range=4.0,
                                  end_of_range=5.0,
                                  commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)
        >> number_range.to_json()
            {"start_of_range": 4.0, "end_of_range": 5.0, "commodity_quantity": "ELECTRIC.POWER.L1"}
        >> json_str = '{"start_of_range": 4.0, "end_of_range": 5.0, "commodity_quantity": "ELECTRIC.POWER.L1"}'
        >> PowerRange.from_json(json_str)


Development
-------------

For development, you can install the required dependencies using the following command:

    pip install -e .[testing,development]


The tests can be run using tox:

    tox

To build the package, you can use tox as well:

    tox -e build,clean
    


