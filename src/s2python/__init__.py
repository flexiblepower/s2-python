import sys  # pragma: no cover
from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "s2-python"  # pylint: disable=invalid-name
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

    from s2python.communication.s2_connection import S2Connection, AssetDetails   # pragma: no cover
    sys.modules['s2python.s2_connection'] = sys.modules['s2python.communication.s2_connection'] # pragma: no cover
