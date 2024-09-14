import importlib_metadata as metadata

try:
    __version__ = metadata.version("gepwc")
except metadata.PackageNotFoundError:
    __version__ = "Package not found"

