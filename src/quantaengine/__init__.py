"""Compatibility namespace for the legacy lattice prototype.

New code should import :mod:`quantaengine_lattice` directly.
"""

from __future__ import annotations

import importlib
import sys
import warnings

from quantaengine_lattice import *  # noqa: F403
from quantaengine_lattice import __all__ as __all__
from quantaengine_lattice import __version__ as __version__

warnings.warn(
    "'quantaengine' is deprecated; import 'quantaengine_lattice' instead",
    DeprecationWarning,
    stacklevel=2,
)

_SUBMODULES = (
    "analysis",
    "chaos",
    "cli",
    "constants",
    "cosmology",
    "engine",
    "fields",
    "io",
    "laws",
    "params",
    "spectrum",
    "visualize",
)
for _name in _SUBMODULES:
    sys.modules[f"{__name__}.{_name}"] = importlib.import_module(f"quantaengine_lattice.{_name}")
