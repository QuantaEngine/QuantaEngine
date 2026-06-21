"""Round-robin tournament: every pair duels; theories scored multi-objectively."""

from __future__ import annotations

import itertools
from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel, Field

from . import scoring
from .cards import JudgeResult, PatchEvent
from .duel import DuelReport, run_duel
from .patchgate import PatchGate
from .registry import TheoryRegistry
from .scoring import TheoryScoreVector
from .theory import TheorySpec


class TournamentReport(BaseModel):
    generation: int = 0
    duels: list[DuelReport] = Field(default_factory=list)
    scores: list[TheoryScoreVector] = Field(default_factory=list)
    pareto_front: list[str] = Field(default_factory=list)
    family_elites: dict[str, list[str]] = Field(default_factory=dict)
    allow_merge: bool = False


def run_tournament(
    theories: list[TheorySpec],
    registry: TheoryRegistry,
    rounds: int = 1,
    generation: int = 0,
    history_dir: str | None = None,
    parallel: bool = True,
    run_seed: int = 0,
    novelty_archive: list[list[float]] | None = None,
) -> TournamentReport:
    pairs = list(itertools.combinations(theories, 2))
    snapshot = registry.all()

    def _duel(pair):
        a, b = pair
        isolated = TheoryRegistry.from_theories(snapshot, policy=registry.policy)
        return run_duel(a, b, isolated, rounds=rounds, run_seed=run_seed)

    if parallel and len(pairs) > 1:
        with ThreadPoolExecutor(max_workers=min(4, len(pairs))) as pool:
            duels = list(pool.map(_duel, pairs))
    else:
        duels = [_duel(p) for p in pairs]

    # Evaluations may run in parallel, but lineage mutations are replayed onto the
    # canonical registry in pair/round/challenge order for deterministic commits.
    gate = PatchGate(registry, history_dir=history_dir, run_seed=run_seed)
    judge_by_target: dict[str, list[JudgeResult]] = {}
    events_by_target: dict[str, list[PatchEvent]] = {}
    for duel in duels:
        for duel_round in duel.rounds:
            decisions_by_target: dict[str, list[tuple]] = {}
            challenge_by_id = {
                challenge.challenge_id: challenge for challenge in duel_round.challenges
            }
            for result in duel_round.judge_results:
                challenge = challenge_by_id[result.challenge_id]
                decisions_by_target.setdefault(result.target_theory_id, []).append(
                    (challenge, result)
                )
            canonical_events: list[PatchEvent] = []
            for target_id, decisions in decisions_by_target.items():
                target = registry.get(target_id)
                _, events = gate.process(target, decisions)
                canonical_events.extend(events)
                judge_by_target.setdefault(target_id, []).extend(result for _, result in decisions)
                events_by_target.setdefault(target_id, []).extend(events)
            duel_round.patch_events = canonical_events

    # rescore current registry theories (patches/forks may have appeared)
    current = registry.all()
    scores = []
    for theory in current:
        penalty, invalidated = scoring.adversarial_outcome(
            judge_by_target.get(theory.theory_id, []),
            events_by_target.get(theory.theory_id, []),
        )
        scores.append(
            scoring.score_theory(
                theory,
                generation=generation,
                unresolved_penalty=penalty,
                invalidated=invalidated,
                run_seed=run_seed,
            )
        )

    # Novelty uses behavior features and excludes the current theory by index.
    current_features = [
        scoring.bridge.novelty_features(theory, scoring.bridge.seed_vector(theory))
        for theory in current
    ]
    historical_features = list(novelty_archive or [])
    for index, score in enumerate(scores):
        feats = current_features[index]
        others = historical_features + [
            feature for other_index, feature in enumerate(current_features) if other_index != index
        ]
        score.novelty = scoring.novelty_score(feats, others)

    front = scoring.pareto_front(scores)
    elites = scoring.family_elites(scores)
    return TournamentReport(
        generation=generation,
        duels=duels,
        scores=scores,
        pareto_front=[s.theory_id for s in front],
        family_elites={fam: [s.theory_id for s in es] for fam, es in elites.items()},
    )
