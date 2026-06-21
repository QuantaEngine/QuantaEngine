"""Enforce total and critical-module coverage contracts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
THRESHOLDS = {
    "total": 90.0,
    "src/cosmogenesis/arena/patchgate.py": 85.0,
    "src/cosmogenesis/cli.py": 85.0,
}


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="quanta-coverage-") as temp:
        report = Path(temp) / "coverage.json"
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "--cov=src/cosmogenesis",
                f"--cov-report=json:{report}",
                "-q",
            ],
            cwd=ROOT,
            check=False,
        )
        if completed.returncode:
            return completed.returncode
        data = json.loads(report.read_text(encoding="utf-8"))

    normalized = {path.replace("\\", "/"): value for path, value in data["files"].items()}
    measured = {"total": float(data["totals"]["percent_covered"])}
    for path in THRESHOLDS:
        if path == "total":
            continue
        measured[path] = float(normalized[path]["summary"]["percent_covered"])

    failed = False
    for name, minimum in THRESHOLDS.items():
        actual = measured[name]
        status = "PASS" if actual >= minimum else "FAIL"
        print(f"[{status}] {name}: {actual:.2f}% (minimum {minimum:.2f}%)")
        failed |= actual < minimum
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
