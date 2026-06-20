"""Adversarial co-training arena: two schemes optimize independently, critique
each other, and consider each other's suggestions until they converge on a
universe that is self-consistent under BOTH paradigms."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from quanta_engine.core.schema import UniverseConfig, load_config

from .parameters import ParameterVector, apply_vector, vector_from_config
from .scheme_a import SchemeA
from .scheme_b import SchemeB


@dataclass(slots=True)
class RoundLog:
    round: int
    champion_a: dict[str, float]
    champion_b: dict[str, float]
    score_a_on_a: float
    score_b_on_b: float
    score_a_on_b: float  # A's verdict on B's champion
    score_b_on_a: float  # B's verdict on A's champion
    disagreement: float
    critique_a_to_b: str
    critique_b_to_a: str
    b_accepted_a: bool
    a_accepted_b: bool


@dataclass(slots=True)
class ArenaResult:
    base_config_name: str
    rounds: list[RoundLog] = field(default_factory=list)
    consensus_vector: dict[str, float] = field(default_factory=dict)
    consensus_score_a: float = 0.0
    consensus_score_b: float = 0.0
    final_disagreement: float = 0.0
    converged: bool = False


def _disagreement(a: SchemeA, b: SchemeB, probes: list[ParameterVector]) -> float:
    diffs = [abs(a.assess(v).score - b.assess(v).score) for v in probes]
    return float(np.mean(diffs)) if diffs else 0.0


def _probe_set(rng: np.random.Generator, anchors: list[ParameterVector], n: int = 6) -> list[ParameterVector]:
    probes = list(anchors)
    for _ in range(n):
        probes.append(ParameterVector.from_normalized(list(rng.random(len(anchors[0].values)))))
    return probes


class Arena:
    def __init__(
        self,
        base_config: UniverseConfig,
        seed: int = 7,
        start: ParameterVector | None = None,
    ) -> None:
        self.base_config = base_config
        self.a = SchemeA(base_config)
        self.b = SchemeB(base_config, seed=seed)
        self.rng = np.random.default_rng(seed)
        start = (start or vector_from_config(base_config)).copy()
        self.a.last_champion = start.copy()
        self.b.last_champion = start.copy()
        # A FIXED probe set so the A/B disagreement is comparable across rounds.
        self._fixed_probes = _probe_set(self.rng, [start], n=8)

    def run(self, rounds: int = 6, tol: float = 0.05, budget: int = 70) -> ArenaResult:
        result = ArenaResult(base_config_name=self.base_config.universe.name)
        for r in range(1, rounds + 1):
            # 1. independent optimization
            champ_a = self.a.optimize(self.a.last_champion, budget=budget)
            champ_b = self.b.optimize(self.b.last_champion, budget=budget)

            # 2. cross-evaluation
            sa_a = self.a.assess(champ_a).score
            sb_b = self.b.assess(champ_b).score
            sa_b = self.a.assess(champ_b).score
            sb_a = self.b.assess(champ_a).score

            # 3. mutual critique
            crit_a = self.a.critique(champ_b, self.b)  # A criticizes B's champion
            crit_b = self.b.critique(champ_a, self.a)  # B criticizes A's champion

            # 4. each evaluates and considers the other's critique
            b_accepted = self.b.consider(crit_a, rival=self.a)
            a_accepted = self.a.consider(crit_b, rival=self.b)

            # disagreement on a fixed probe set PLUS the two current champions.
            probes = [*self._fixed_probes, self.a.last_champion, self.b.last_champion]
            disagreement = _disagreement(self.a, self.b, probes)

            result.rounds.append(
                RoundLog(
                    round=r,
                    champion_a=champ_a.as_dict(),
                    champion_b=champ_b.as_dict(),
                    score_a_on_a=sa_a,
                    score_b_on_b=sb_b,
                    score_a_on_b=sa_b,
                    score_b_on_a=sb_a,
                    disagreement=disagreement,
                    critique_a_to_b=crit_a.weakness,
                    critique_b_to_a=crit_b.weakness,
                    b_accepted_a=b_accepted,
                    a_accepted_b=a_accepted,
                )
            )
            # Convergence is about both paradigms ENDORSING each other's champion
            # (cross-scores high and close to own scores), not about agreeing on
            # the whole random landscape -- that residual gap is the genuine,
            # expected difference between the two paradigms.
            cross_gap = max(abs(sa_a - sb_a), abs(sb_b - sa_b))
            if cross_gap < tol and min(sa_a, sb_b, sa_b, sb_a) > 0.6:
                result.converged = True
                break

        # consensus: maximize min(score_A, score_B) over champions + midpoint
        candidates = [self.a.last_champion, self.b.last_champion]
        mid = ParameterVector.from_normalized(
            list(
                0.5
                * (
                    np.array(self.a.last_champion.to_normalized())
                    + np.array(self.b.last_champion.to_normalized())
                )
            )
        )
        candidates.append(mid)
        best = max(candidates, key=lambda v: min(self.a.assess(v).score, self.b.assess(v).score))
        result.consensus_vector = best.as_dict()
        result.consensus_score_a = self.a.assess(best).score
        result.consensus_score_b = self.b.assess(best).score
        result.final_disagreement = result.rounds[-1].disagreement if result.rounds else 0.0
        self._consensus_vector = best
        return result

    def consensus_config(self, result: ArenaResult) -> UniverseConfig:
        return apply_vector(self.base_config, self._consensus_vector)


def run_adversarial(
    base: str | Path | UniverseConfig,
    rounds: int = 6,
    out_dir: str | Path | None = None,
    seed: int = 7,
    budget: int = 70,
    start: ParameterVector | None = None,
) -> ArenaResult:
    """End-to-end adversarial universe generation + iterative co-optimization."""

    config = base if isinstance(base, UniverseConfig) else load_config(base)
    arena = Arena(config, seed=seed, start=start)
    result = arena.run(rounds=rounds, budget=budget)
    if out_dir is not None:
        _write_artifacts(arena, result, Path(out_dir))
    return result


def _write_artifacts(arena: Arena, result: ArenaResult, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "arena_result.json").write_text(
        json.dumps(_result_to_dict(result), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (out_dir / "arena_report.md").write_text(_render_markdown(result), encoding="utf-8")

    # consensus universe config + its dual report
    consensus_cfg = arena.consensus_config(result)
    import yaml

    (out_dir / "consensus_universe.yaml").write_text(
        yaml.safe_dump(consensus_cfg.model_dump(), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        rounds = [r.round for r in result.rounds]
        if rounds:
            fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
            ax.plot(rounds, [r.disagreement for r in result.rounds], "o-", label="A/B disagreement")
            ax.plot(rounds, [r.score_a_on_a for r in result.rounds], "s--", label="A score (own)")
            ax.plot(rounds, [r.score_b_on_b for r in result.rounds], "^--", label="B score (own)")
            ax.plot(rounds, [r.score_a_on_b for r in result.rounds], "x:", label="A scores B")
            ax.plot(rounds, [r.score_b_on_a for r in result.rounds], "+:", label="B scores A")
            ax.set_xlabel("adversarial round")
            ax.set_ylabel("score / disagreement")
            ax.set_ylim(-0.02, 1.05)
            ax.grid(alpha=0.25)
            ax.legend(fontsize=8)
            fig.savefig(out_dir / "convergence.png", dpi=150)
            plt.close(fig)
    except Exception:  # plotting is best-effort
        pass


def _result_to_dict(result: ArenaResult) -> dict[str, Any]:
    return {
        "base_config_name": result.base_config_name,
        "converged": result.converged,
        "final_disagreement": result.final_disagreement,
        "consensus_vector": result.consensus_vector,
        "consensus_score_a": result.consensus_score_a,
        "consensus_score_b": result.consensus_score_b,
        "rounds": [asdict(r) for r in result.rounds],
    }


def _render_markdown(result: ArenaResult) -> str:
    lines = [
        f"# Adversarial Cosmogenesis Report: {result.base_config_name}",
        "",
        "Two independent paradigms (A: analytic forward compiler, B: variational "
        "self-consistency relaxation) generated and adversarially co-optimized universes.",
        "",
        "## Convergence",
        f"- Converged: **{result.converged}**",
        f"- Final A/B disagreement: **{result.final_disagreement:.4f}**",
        f"- Consensus score (A): **{result.consensus_score_a:.4f}**",
        f"- Consensus score (B): **{result.consensus_score_b:.4f}**",
        "",
        "## Consensus Universe (robust under both paradigms)",
        "```",
        json.dumps(result.consensus_vector, indent=2),
        "```",
        "",
        "## Round-by-round adversarial log",
        "",
        "| r | A(own) | B(own) | A→B | B→A | disagree | B took A | A took B |",
        "|---|--------|--------|-----|-----|----------|----------|----------|",
    ]
    for r in result.rounds:
        lines.append(
            f"| {r.round} | {r.score_a_on_a:.3f} | {r.score_b_on_b:.3f} | "
            f"{r.score_a_on_b:.3f} | {r.score_b_on_a:.3f} | {r.disagreement:.3f} | "
            f"{'yes' if r.b_accepted_a else 'no'} | {'yes' if r.a_accepted_b else 'no'} |"
        )
    lines.append("")
    lines.append("## Exchanged critiques")
    for r in result.rounds:
        lines.append(f"\n### Round {r.round}")
        lines.append(f"- **A → B:** {r.critique_a_to_b}")
        lines.append(f"- **B → A:** {r.critique_b_to_a}")
    lines.append("")
    lines.append(
        "> Scores are physical-feasibility heuristics under each paradigm, not "
        "probabilities. Convergence means both independent models agree the universe "
        "is self-consistent."
    )
    return "\n".join(lines)
