"""GenesisArena: a parallel, multi-lineage, adversarial universe-generation platform.

Multiple physics paradigms (analytic / variational / minimal-axiom) live as
independent theory lineages that challenge each other, are judged by a
deterministic verifier, and are patched or forked locally -- but never merged
into a single winner. Selection keeps a Pareto front + family elites + a novelty
archive, so a diverse ecosystem of self-consistent universes is preserved.

See plans/2026-06-21-GENESIS_ARENA_V2_PARALLEL_ADVERSARIAL.md.
"""

from .duel import DuelReport, run_duel
from .evolution import EvolutionReport, evolve
from .theory import TheoryRegistry, TheorySpec, load_theory
from .tournament import TournamentReport, run_tournament

__all__ = [
    "TheorySpec",
    "TheoryRegistry",
    "load_theory",
    "run_duel",
    "DuelReport",
    "run_tournament",
    "TournamentReport",
    "evolve",
    "EvolutionReport",
]

__version__ = "2.0.0"
