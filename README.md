# Python Wrapper for S2 Flexibility Protocol

<div align="center">
    <a href="https://s2standard.org"><img src="./Logo-S2.svg" width="200" height="200" /></a>
    <div>
        <a href="https://pypi.org/project/s2-python/"><img src="https://img.shields.io/pypi/v/s2-python" /></a>
        <a href="https://pypi.org/project/s2-python/"><img src="https://img.shields.io/pypi/pyversions/s2-python" /></a>
    </div>
    <div>
        <a href="./LICENSE"><img src="https://img.shields.io/pypi/l/s2-python" /></a>
        <a href="https://discord.com/invite/NyFMEPmuDw"><img src="https://img.shields.io/discord/1351281839913832510"></a>
    </div>
</div>
<br />

This Python package implements the message validation for the EN50491-12-2 "S2" standard for home and building energy management. This implementation
is based on the asyncapi description of the protocol provided in the [s2-ws-json](https://github.com/flexiblepower/s2-ws-json/) repository. 

## To Install
You can install this package using pip or any Python dependency manager that collects the packages from PyPI:

```bash
pip install s2-python
pip install s2-python[ws]  # for S2 over WebSockets
```

The packages on PyPI may be found [here](https://pypi.org/project/s2-python/).

## Mypy support
s2-python uses pydantic at its core to define the various S2 messages. As such, the pydantic mypy plugin is required
for type checking to succeed.

Add to your pyproject.toml:

```toml
[tool.mypy]
plugins = ['pydantic.mypy']
```


## Example

```python
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
```

## Development

For development, you can install the required dependencies using the following command:
```bash
    pip install -e .[testing,development,ws]
```

The tests can be run using tox:
```bash
    tox
```

To build the package, you can use tox as well:
```bash
    tox -e build,clean
```

## Funding Acknowledgements
This project is co-financed by [TKI-Energie](https://topsectorenergie.nl/nl/maak-kennis-met-tse/tki-energie-en-industrie/) from the Top Consortia for Knowledge and Innovation (TKI) surcharge of
the Ministry of Economic Affairs and Climate Policy.
