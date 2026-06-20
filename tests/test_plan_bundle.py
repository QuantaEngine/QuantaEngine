import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
PACKAGE = ROOT / "plans" / "quantaengine-mvp-v1"


def test_plan_manifest_links_existing_inputs_and_artifacts():
    manifest = yaml.safe_load((PACKAGE / "PLAN_MANIFEST.yaml").read_text(encoding="utf-8"))
    assert manifest["plan_id"] == "quantaengine-mvp-v1"
    assert (PACKAGE / manifest["canonical_plan"]).resolve().is_file()
    assert manifest["scope"]["included_stages"] == list(range(12))
    for artifact in manifest["artifacts"]:
        assert (ROOT / artifact).is_file()


def test_plan_bundle_relative_markdown_links_resolve():
    link_pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for document in [ROOT / "plans" / "README.md", *PACKAGE.glob("*.md")]:
        for target in link_pattern.findall(document.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            relative_target = target.split("#", 1)[0]
            assert (document.parent / relative_target).resolve().exists(), (
                f"broken link in {document.relative_to(ROOT)}: {target}"
            )


def test_acceptance_runner_executes_scenarios(tmp_path: Path):
    evidence = tmp_path / "evidence.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(PACKAGE / "execution" / "run_acceptance.py"),
            "--skip-tooling",
            "--artifact-dir",
            str(tmp_path / "artifacts"),
            "--evidence",
            str(evidence),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    data = json.loads(evidence.read_text(encoding="utf-8"))
    assert data["acceptance_passed"] is True
    assert all(data["assertions"].values())
    assert data["scenarios"]["standard"]["final_verdict"] == "civilization window plausible"
