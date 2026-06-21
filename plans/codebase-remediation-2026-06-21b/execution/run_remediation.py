"""Execute and archive round-B remediation quality gates."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import venv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RECORD = ROOT / "plans/codebase-remediation-2026-06-21b/records/remediation-evidence.json"


def run(check_id: str, command: list[str], cwd: Path = ROOT) -> dict[str, object]:
    started = time.monotonic()
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part).strip()
    return {
        "id": check_id,
        "command": command,
        "returncode": completed.returncode,
        "duration_seconds": round(time.monotonic() - started, 3),
        "status": "passed" if completed.returncode == 0 else "failed",
        "output_tail": output[-5000:],
    }


def wheel_smoke() -> dict[str, object]:
    wheels = sorted((ROOT / "dist").glob("quanta_engine-*.whl"), key=os.path.getmtime)
    if not wheels:
        return {
            "id": "wheel-smoke",
            "command": [],
            "returncode": 1,
            "duration_seconds": 0.0,
            "status": "failed",
            "output_tail": "no wheel found under dist/",
        }
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="quanta-b-wheel-") as temp:
        temp_path = Path(temp)
        env_dir = temp_path / "venv"
        venv.EnvBuilder(with_pip=True, system_site_packages=True).create(env_dir)
        python = env_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        commands = [
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--no-deps",
                "--force-reinstall",
                str(wheels[-1]),
            ],
            [
                str(python),
                "-c",
                (
                    "import cosmogenesis, quanta_engine, quantaengine_lattice; "
                    "from cosmogenesis import list_schemes; "
                    "assert cosmogenesis.__version__ == quanta_engine.__version__ == "
                    "quantaengine_lattice.__version__ == '0.3.0'; "
                    "assert set(list_schemes()) == "
                    "{'analytic_compiler', 'variational_relaxer', 'minimal_axiom'}"
                ),
            ],
            [
                str(python),
                "-m",
                "cosmogenesis",
                "--workspace",
                str(ROOT),
                "theory-list",
            ],
        ]
        outputs: list[str] = []
        returncode = 0
        for command in commands:
            completed = subprocess.run(
                command, cwd=temp_path, capture_output=True, text=True, check=False
            )
            outputs.append(completed.stdout + completed.stderr)
            if completed.returncode:
                returncode = completed.returncode
                break
    return {
        "id": "wheel-smoke",
        "command": commands,
        "returncode": returncode,
        "duration_seconds": round(time.monotonic() - started, 3),
        "status": "passed" if returncode == 0 else "failed",
        "output_tail": "\n".join(outputs)[-5000:],
    }


def revision() -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-wheel-smoke", action="store_true")
    args = parser.parse_args()
    python = sys.executable
    scopes = [
        "src",
        "tests",
        "examples",
        "plans/quantaengine-mvp-v1/execution",
        "plans/codebase-remediation-2026-06-21/execution",
        "plans/codebase-remediation-2026-06-21b/execution",
    ]
    commands = [
        (
            "round-b-regressions",
            [
                python,
                "-m",
                "pytest",
                "tests/test_remediation_b.py",
                "tests/test_physics_invariants.py",
                "-q",
            ],
        ),
        (
            "coverage-contracts",
            [python, "plans/codebase-remediation-2026-06-21/execution/check_coverage.py"],
        ),
        ("full-tests", [python, "-m", "pytest"]),
        ("lint", [python, "-m", "ruff", "check", *scopes]),
        ("format", [python, "-m", "ruff", "format", "--check", *scopes]),
        ("types", [python, "-m", "mypy", "src"]),
        ("dependencies", [python, "-m", "pip", "check"]),
        ("build", [python, "-m", "build"]),
    ]
    checks: list[dict[str, object]] = []
    for check_id, command in commands:
        result = run(check_id, command)
        checks.append(result)
        print(f"[{result['status']}] {check_id}")
        if result["returncode"] != 0:
            break
    if checks and checks[-1]["returncode"] == 0 and not args.skip_wheel_smoke:
        result = wheel_smoke()
        checks.append(result)
        print(f"[{result['status']}] wheel-smoke")

    passed = bool(checks) and all(check["returncode"] == 0 for check in checks)
    evidence = {
        "plan_id": "codebase-remediation-2026-06-21b",
        "status": "passed" if passed else "failed",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "revision": revision(),
        "python": sys.version,
        "checks": checks,
    }
    RECORD.parent.mkdir(parents=True, exist_ok=True)
    temp_record = RECORD.with_suffix(".tmp")
    temp_record.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
    shutil.move(temp_record, RECORD)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
