"""Regression evidence for the 2026-06-21 codebase assessment."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

import cosmogenesis
import quanta_engine
import quantaengine_lattice
from cosmogenesis.arena import bridge, scoring
from cosmogenesis.arena.cards import (
    ChallengeCard,
    ChallengeType,
    JudgeDecision,
    JudgeResult,
    PatchEvent,
    PatchOutcome,
    Severity,
)
from cosmogenesis.arena.ledger import append_history
from cosmogenesis.arena.patchgate import PatchGate
from cosmogenesis.arena.registry import TheoryRegistry
from cosmogenesis.arena.tournament import run_tournament
from cosmogenesis.cli import app
from cosmogenesis.core import ParameterVector, UniverseAssessment

ROOT = Path(__file__).parents[1]
THEORIES = ROOT / "theories"


def _fork_decision(target_id: str, challenge_id: str) -> tuple[ChallengeCard, JudgeResult]:
    challenge = ChallengeCard(
        challenge_id=challenge_id,
        source_theory_id="T-0001",
        target_theory_id=target_id,
        challenge_type=ChallengeType.OVERFITTING_TO_STANDARD_UNIVERSE,
        severity=Severity.MINOR,
        summary="concurrent fork regression",
        suggested_resolution="fork",
    )
    result = JudgeResult(
        judge_result_id=f"J-{challenge_id}",
        challenge_id=challenge_id,
        target_theory_id=target_id,
        decision=JudgeDecision.FORK_RECOMMENDED,
        severity=Severity.MINOR,
        rationale="verified",
        fork_recommended=True,
    )
    return challenge, result


def test_concurrent_forks_allocate_unique_ids() -> None:
    source = TheoryRegistry.from_dir(THEORIES).get("T-0002")
    roots = [
        source.model_copy(update={"theory_id": f"T-{1000 + index:04d}"}) for index in range(100)
    ]
    registry = TheoryRegistry.from_theories(roots)
    gate = PatchGate(registry, run_seed=17)

    def fork(root_index: int) -> str | None:
        target = roots[root_index]
        challenge, result = _fork_decision(target.theory_id, f"CH-{root_index:04d}")
        return gate.process(target, [(challenge, result)])[1][0].child_theory_id

    with ThreadPoolExecutor(max_workers=16) as pool:
        child_ids = list(pool.map(fork, range(len(roots))))

    assert all(child_ids)
    assert len(set(child_ids)) == len(roots)
    assert len(registry.all()) == len(roots) * 2


def test_parallel_and_serial_tournaments_are_identical() -> None:
    source = TheoryRegistry.from_dir(THEORIES)
    serial_registry = TheoryRegistry.from_theories(source.all(), policy=source.policy)
    parallel_registry = TheoryRegistry.from_theories(source.all(), policy=source.policy)
    serial = run_tournament(
        serial_registry.all(), serial_registry, parallel=False, run_seed=1234
    ).model_dump()
    parallel = run_tournament(
        parallel_registry.all(), parallel_registry, parallel=True, run_seed=1234
    ).model_dump()
    assert parallel == serial
    assert [theory.model_dump() for theory in parallel_registry.all()] == [
        theory.model_dump() for theory in serial_registry.all()
    ]


def test_stable_seed_ignores_python_hash_salt() -> None:
    script = """
import json
from cosmogenesis.arena.patchgate import PatchGate
from cosmogenesis.arena.registry import TheoryRegistry
registry = TheoryRegistry.from_dir('theories')
theory = registry.get('T-0001')
print(json.dumps(PatchGate(registry, run_seed=91)._robust_reseed(theory, samples=5).values))
"""
    outputs = []
    for hash_seed in ("1", "987654"):
        env = {**os.environ, "PYTHONHASHSEED": hash_seed}
        outputs.append(
            subprocess.check_output(
                [sys.executable, "-c", script], cwd=ROOT, env=env, text=True
            ).strip()
        )
    assert outputs[0] == outputs[1]


def test_novelty_excludes_self_and_uses_behavior_features() -> None:
    registry = TheoryRegistry.from_dir(THEORIES)
    report = run_tournament(registry.all(), registry, run_seed=7)
    assert any(score.novelty > 0.0 for score in report.scores)
    assert all(0.0 <= score.novelty <= 1.0 for score in report.scores)


def test_adversarial_outcome_changes_score_and_handles_invalidation() -> None:
    registry = TheoryRegistry.from_dir(THEORIES)
    theory = registry.get("T-0001")
    _, unresolved = _fork_decision(theory.theory_id, "CH-unresolved")
    penalty, invalidated = scoring.adversarial_outcome([unresolved], [])
    clean = scoring.score_theory(theory, run_seed=3)
    penalized = scoring.score_theory(theory, unresolved_penalty=penalty, run_seed=3)
    assert penalty == 1.0 and not invalidated
    assert penalized.display_score < clean.display_score
    assert scoring.pareto_dominates(clean, penalized)

    invalidation = PatchEvent(
        theory_id=theory.theory_id,
        based_on_challenge_id=unresolved.challenge_id,
        outcome=PatchOutcome.INVALIDATED,
        summary="invalid",
    )
    penalty, invalidated = scoring.adversarial_outcome([unresolved], [invalidation])
    invalid = scoring.score_theory(
        theory, unresolved_penalty=penalty, invalidated=invalidated, run_seed=3
    )
    assert invalid.validity == invalid.physical_consistency == 0.0
    assert invalid.unresolved_challenge_penalty == 1.0


def test_legacy_namespace_and_versions_are_consistent() -> None:
    with pytest.warns(DeprecationWarning):
        import quantaengine
    from quantaengine.cosmology import FriedmannBackground

    assert FriedmannBackground.__module__ == "quantaengine_lattice.cosmology"
    assert {
        quanta_engine.__version__,
        cosmogenesis.__version__,
        quantaengine_lattice.__version__,
        quantaengine.__version__,
    } == {"0.3.0"}


def test_theory_config_resolution_is_independent_of_cwd(tmp_path: Path, monkeypatch) -> None:
    theory_path = THEORIES / "T-0001_conservative_eft" / "theory.yaml"
    registry = TheoryRegistry.from_dir(THEORIES)
    theory = registry.get("T-0001")
    monkeypatch.chdir(tmp_path)
    assert theory.resolve_base_config() == ROOT / "configs" / "standard_universe.yaml"
    assert bridge.assess(theory, bridge.seed_vector(theory)).score > 0.9
    assert theory_path.is_file()


def test_cli_workspace_and_version_from_arbitrary_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)
    version = runner.invoke(app, ["--version"])
    assert version.exit_code == 0
    assert "0.3.0" in version.stdout
    result = runner.invoke(
        app,
        ["--workspace", str(ROOT), "theory-list"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert "T-0001" in result.stdout
    duel = runner.invoke(
        app,
        [
            "--workspace",
            str(ROOT),
            "duel",
            "theories/T-0001_conservative_eft/theory.yaml",
            "theories/T-0003_minimal_axiom/theory.yaml",
            "--seed",
            "9",
        ],
        catch_exceptions=False,
    )
    assert duel.exit_code == 0
    assert "merged_theory_id: None" in duel.stdout
    assert not (tmp_path / "theories").exists()


def test_evolution_populates_novelty_archive() -> None:
    from cosmogenesis.arena.evolution import evolve

    registry = TheoryRegistry.from_dir(THEORIES)
    report = evolve(
        registry.all(),
        registry,
        generations=1,
        optimize_budget=2,
        parallel=False,
        run_seed=7,
    )
    assert report.archive_ids


def test_log_axis_uses_equal_decade_steps() -> None:
    normalized = [
        ParameterVector([1.0, gravity, 1.0, 1.0, -8.0]).to_normalized()[1]
        for gravity in (0.01, 0.1, 1.0, 10.0, 100.0)
    ]
    assert normalized == pytest.approx([0.0, 0.25, 0.5, 0.75, 1.0])


def test_registry_manifest_is_enforced(tmp_path: Path) -> None:
    copied = tmp_path / "theories"
    shutil.copytree(THEORIES, copied)
    manifest_path = copied / "registry.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["theories"][0]["family"] = "wrong_family"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    with pytest.raises(ValueError, match="does not match"):
        TheoryRegistry.from_dir(copied)


def test_history_has_global_sequence_and_run_identity(tmp_path: Path) -> None:
    registry = TheoryRegistry.from_dir(THEORIES)
    theory = registry.get("T-0001")
    score = scoring.score_theory(theory, run_seed=5)
    root = tmp_path / "theories"
    for run_id, run_generation in (("RUN-A", 7), ("RUN-B", 0)):
        append_history(
            theory,
            run_generation,
            score,
            [],
            root=root,
            persist_spec=True,
            run_id=run_id,
            run_seed=5,
        )
    history = next(root.glob("T-0001_*/history.jsonl"))
    records = [json.loads(line) for line in history.read_text(encoding="utf-8").splitlines()]
    assert [record["generation"] for record in records] == [0, 1]
    assert [record["run_generation"] for record in records] == [7, 0]
    assert [record["run_id"] for record in records] == ["RUN-A", "RUN-B"]
    assert all(record["theory_fingerprint"] and record["config_sha256"] for record in records)


@pytest.mark.parametrize(
    ("field", "value"),
    (("score", float("nan")), ("score", 1.1), ("residual", -0.1)),
)
def test_assessment_rejects_invalid_numeric_contract(field: str, value: float) -> None:
    kwargs = {"scheme": "test", "score": 0.5, "feasible": True, "residual": 0.0}
    kwargs[field] = value
    with pytest.raises(ValueError):
        UniverseAssessment(**kwargs)
