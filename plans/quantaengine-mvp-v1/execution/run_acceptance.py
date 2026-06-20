"""Rebuild and verify all QuantaEngine MVP acceptance evidence."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from quanta_engine.experiments.scan import save_scan_artifacts, scan_parameter
from quanta_engine.pipeline import run_universe_pipeline

PACKAGE_DIR = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MANIFEST = PACKAGE_DIR / "PLAN_MANIFEST.yaml"
DEFAULT_EVIDENCE = PACKAGE_DIR / "records" / "acceptance-evidence.json"


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def load_manifest(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("plan_id") != "quantaengine-mvp-v1":
        raise ValueError("manifest must describe plan_id quantaengine-mvp-v1")
    return data


def run_tooling(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    for check in manifest["tooling"]:
        command = [sys.executable if part == "{python}" else str(part) for part in check["command"]]
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        output = "\n".join(
            part for part in (completed.stdout.strip(), completed.stderr.strip()) if part
        )
        summary = next(
            (line for line in reversed(output.splitlines()) if line.strip()), "no output"
        )
        results[check["id"]] = {
            "passed": completed.returncode == 0,
            "command": command,
            "summary": summary,
        }
    return results


def _standard_facts(report: Any) -> dict[str, Any]:
    return {
        "validation_passed": report.validation_report.passed,
        "stable_hydrogen": report.atomic_report.stable_hydrogen,
        "hydrogen_binding_energy_eV": report.atomic_report.binding_energy_eV,
        "bohr_radius_m": report.atomic_report.bohr_radius_m,
        "deuteron_stable": report.nuclear_report.deuteron_stable,
        "helium4_stable": report.nuclear_report.helium4_stable,
        "universe_age_Gyr": report.cosmology_report.age_of_universe_Gyr,
        "hydrogen_fusion_possible": report.stellar_report.hydrogen_fusion_possible,
        "long_lived_stars_possible": report.stellar_report.long_lived_stars_possible,
        "stellar_lifetime_years": report.stellar_report.characteristic_stellar_lifetime_years,
        "structure_growth_possible": report.structure_report.structure_growth_possible,
        "galaxy_formation_possible": report.structure_report.galaxy_formation_possible,
        "planet_formation_possible": report.structure_report.planet_formation_possible,
        "life_window_score": report.complexity_report.life_window_score,
        "civilization_potential_score": report.complexity_report.civilization_potential_score,
        "final_verdict": report.final_verdict,
    }


def build_scenario_evidence(
    manifest: dict[str, Any], artifact_dir: Path
) -> tuple[dict[str, Any], dict[str, bool], list[str]]:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    standard_spec = manifest["standard_acceptance"]
    standard = run_universe_pipeline(ROOT / standard_spec["config"])
    standard.write(artifact_dir / "standard.md", artifact_dir / "standard.json")
    standard_facts = _standard_facts(standard)

    atomless = run_universe_pipeline(
        ROOT / manifest["variant_acceptance"]["no_stable_atoms"]["config"]
    )
    strong_gravity = run_universe_pipeline(
        ROOT / manifest["variant_acceptance"]["strong_gravity"]["config"]
    )
    smooth = run_universe_pipeline(
        ROOT / manifest["variant_acceptance"]["no_perturbations"]["config"]
    )
    scenarios = {
        "standard": standard_facts,
        "no_stable_atoms": _standard_facts(atomless),
        "strong_gravity": _standard_facts(strong_gravity),
        "no_perturbations": _standard_facts(smooth),
    }

    alpha_spec = manifest["scans"]["alpha"]
    alpha_frame = scan_parameter(
        ROOT / standard_spec["config"], alpha_spec["parameter"], alpha_spec["values"]
    )
    alpha_paths = save_scan_artifacts(
        alpha_frame, artifact_dir / "scan_alpha.csv", alpha_spec["parameter"]
    )
    gravity_spec = manifest["scans"]["gravity"]
    gravity_frame = scan_parameter(
        ROOT / standard_spec["config"], gravity_spec["parameter"], gravity_spec["values"]
    )
    gravity_paths = save_scan_artifacts(
        gravity_frame, artifact_dir / "scan_gravity.csv", gravity_spec["parameter"]
    )

    binding_min, binding_max = standard_spec["hydrogen_binding_energy_eV"]
    radius_min, radius_max = standard_spec["bohr_radius_m"]
    age_min, age_max = standard_spec["universe_age_Gyr"]
    atomless_spec = manifest["variant_acceptance"]["no_stable_atoms"]
    gravity_acceptance = manifest["variant_acceptance"]["strong_gravity"]
    smooth_spec = manifest["variant_acceptance"]["no_perturbations"]
    assertions = {
        "standard_required_flags": all(
            standard_facts[name] for name in standard_spec["required_true"]
        ),
        "standard_binding_energy": binding_min
        <= standard_facts["hydrogen_binding_energy_eV"]
        <= binding_max,
        "standard_bohr_radius": radius_min <= standard_facts["bohr_radius_m"] <= radius_max,
        "standard_universe_age": age_min <= standard_facts["universe_age_Gyr"] <= age_max,
        "standard_life_window": standard_facts["life_window_score"]
        >= standard_spec["minimum_life_window_score"],
        "atomless_hydrogen": atomless.atomic_report.stable_hydrogen
        == atomless_spec["stable_hydrogen"],
        "atomless_life_window": atomless.complexity_report.life_window_score
        <= atomless_spec["maximum_life_window_score"],
        "strong_gravity_long_lived": strong_gravity.stellar_report.long_lived_stars_possible
        == gravity_acceptance["long_lived_stars_possible"],
        "strong_gravity_lifetime": strong_gravity.stellar_report.characteristic_stellar_lifetime_years
        <= gravity_acceptance["maximum_stellar_lifetime_years"],
        "smooth_structure": smooth.structure_report.structure_growth_possible
        == smooth_spec["structure_growth_possible"],
        "smooth_galaxies": smooth.structure_report.galaxy_formation_possible
        == smooth_spec["galaxy_formation_possible"],
        "smooth_planets": smooth.structure_report.planet_formation_possible
        == smooth_spec["planet_formation_possible"],
        "alpha_scan_rows": len(alpha_frame) == len(alpha_spec["values"]),
        "gravity_scan_rows": len(gravity_frame) == len(gravity_spec["values"]),
    }
    artifacts = [artifact_dir / "standard.md", artifact_dir / "standard.json"]
    artifacts.extend(alpha_paths.values())
    artifacts.extend(gravity_paths.values())
    return scenarios, assertions, [_display_path(path) for path in artifacts]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--artifact-dir", type=Path, default=ROOT / "reports")
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument(
        "--skip-tooling", action="store_true", help="Run scenarios only; intended for runner tests."
    )
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    tooling = {"skipped": {"passed": True, "summary": "skipped by request"}}
    if not args.skip_tooling:
        tooling = run_tooling(manifest)
    scenarios, assertions, artifacts = build_scenario_evidence(manifest, args.artifact_dir)
    passed = all(item["passed"] for item in tooling.values()) and all(assertions.values())
    evidence = {
        "schema_version": 1,
        "plan_id": manifest["plan_id"],
        "acceptance_passed": passed,
        "tooling": tooling,
        "assertions": assertions,
        "scenarios": scenarios,
        "artifacts": artifacts,
    }
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Acceptance passed: {passed}")
    print(f"Evidence: {args.evidence.resolve()}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
