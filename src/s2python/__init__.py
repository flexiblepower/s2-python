from importlib.metadata import PackageNotFoundError, version, sys  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "s2-python"  # pylint: disable=invalid-name
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

    from s2python.communication.s2_connection import S2Connection, AssetDetails
    sys.modules['s2python.s2_connection'] = sys.modules.get('s2python.communication.s2_connection', None)
