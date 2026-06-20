"""Adversarial cosmogenesis: two independent universe-generation paradigms that
co-optimize through mutual critique.

- Scheme A (``SchemeA``): analytic forward-pass compiler wrapping ``quanta_engine``.
- Scheme B (``SchemeB``): variational self-consistency field relaxation, built
  from first principles with an explicit cross-layer residual.

Both consume the same ``UniverseConfig`` / parameter vector (shared entry point)
and return a common ``UniverseAssessment``. ``run_adversarial`` drives the
end-to-end generation + iterative adversarial optimization.
"""

from .arena import Arena, ArenaResult, run_adversarial
from .assessment import UniverseAssessment
from .parameters import ParameterVector, apply_vector, vector_from_config
from .scheme_a import SchemeA
from .scheme_b import SchemeB
from .scheme_c import SchemeC

__all__ = [
    "Arena",
    "ArenaResult",
    "run_adversarial",
    "UniverseAssessment",
    "ParameterVector",
    "apply_vector",
    "vector_from_config",
    "SchemeA",
    "SchemeB",
    "SchemeC",
]

__version__ = "0.1.0"
