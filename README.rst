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
You can install this package using pip or any Python dependency manager that collects the packages from PyPI:

.. code-block:: bash

    pip install s2-python
    pip install s2-python[ws]  # for S2 over WebSockets

The packages on PyPI may be found `here <https://pypi.org/project/s2-python/>`_

Mypy support
------------
s2-python uses pydantic at its core to define the various S2 messages. As such, the pydantic mypy plugin is required
for type checking to succeed.

Add to your pyproject.toml:

.. code-block:: toml

    [tool.mypy]
    plugins = ['pydantic.mypy']

Examples
---------

Use S2 classes in your code:

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

Run an example CEM server with websocket and http server:

.. code-block:: bash

    python -m examples.example_s2_server --host localhost --http-port 8000 --ws-port 8080 --pairing-token ca14fda4


This will start both a http and a websocket server instances. It also allows to set a hardcoded pairing token.

Run an example RM client that pairs with the CEM server, authenticates and starts sending S2 messages that describe an FRBC device:

.. code-block:: bash

    python -m examples.example_pairing_frbc_rm --pairing_endpoint http://localhost:8000/requestPairing --pairing_token ca14fda4

In case you want to run the example of a client that does not need to pair with the CEM server, you can add the --dev-mode flag. This will disable the pairing/authentication check and allows you to send messages to the CEM server without pairing. The CEM server still needs to be running.

.. code-block:: bash

    python -m examples.example_frbc_rm --endpoint ws://localhost:8080


Development
-------------

For development, you can install the required dependencies using the following command:

    pip install -e .[testing,development]


The tests can be run using tox:

    tox

To build the package, you can use tox as well:

    tox -e build,clean
    


