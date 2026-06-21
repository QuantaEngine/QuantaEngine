"""QuantaEngine: from fundamental quanta to generated universes."""

from quanta_engine.version import __version__

from .engine import QuantaEngine, UniverseResult
from .laws import LawBook, minimal_lawbook
from .params import UniverseParams

__all__ = [
    "LawBook",
    "QuantaEngine",
    "UniverseParams",
    "UniverseResult",
    "__version__",
    "minimal_lawbook",
]
