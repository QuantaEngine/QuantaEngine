"""Shared adversarial I/O contract for every scheme.

- ``ParameterVector`` is the common, scheme-agnostic search space.
- ``UniverseAssessment`` is the common verdict every scheme returns.
- ``UniverseScheme`` / ``BaseEngine`` is the contract a scheme implements.
"""

from .assessment import UniverseAssessment, logistic_window, softmin
from .parameters import (
    AXES,
    AXIS_BY_NAME,
    NDIM,
    ParameterVector,
    apply_vector,
    vector_from_config,
)
from .protocol import (
    BaseEngine,
    CalibrationThreshold,
    ConsiderDecision,
    UniverseScheme,
    fragility_profile,
)
from .reproducibility import (
    code_revision,
    file_sha256,
    object_fingerprint,
    software_version,
    stable_digest,
    stable_identifier,
    stable_seed,
)

__all__ = [
    "ParameterVector",
    "AXES",
    "AXIS_BY_NAME",
    "NDIM",
    "apply_vector",
    "vector_from_config",
    "UniverseAssessment",
    "softmin",
    "logistic_window",
    "UniverseScheme",
    "BaseEngine",
    "CalibrationThreshold",
    "ConsiderDecision",
    "fragility_profile",
    "stable_digest",
    "stable_seed",
    "stable_identifier",
    "object_fingerprint",
    "file_sha256",
    "software_version",
    "code_revision",
]
