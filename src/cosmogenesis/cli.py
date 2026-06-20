"""CLI for adversarial cosmogenesis."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .arena import run_adversarial

app = typer.Typer(
    name="cosmogenesis",
    help="Generate a self-consistent universe via two adversarially co-trained paradigms.",
    no_args_is_help=True,
)
console = Console()


@app.callback()
def _root() -> None:
    """Adversarial cosmogenesis CLI."""


@app.command("run-adversarial")
def run_adversarial_cmd(
    base: Annotated[Path, typer.Option("--base", exists=True, dir_okay=False)],
    rounds: Annotated[int, typer.Option("--rounds", help="Adversarial rounds.")] = 6,
    out: Annotated[Path | None, typer.Option("--out", help="Output directory.")] = None,
    seed: Annotated[int, typer.Option("--seed")] = 7,
    budget: Annotated[int, typer.Option("--budget", help="Evals per optimizer call.")] = 70,
) -> None:
    result = run_adversarial(base, rounds=rounds, out_dir=out, seed=seed, budget=budget)
    console.print(f"[bold]Base:[/bold] {result.base_config_name}")
    console.print(f"Converged: {result.converged} (rounds run: {len(result.rounds)})")
    console.print(f"Final disagreement: {result.final_disagreement:.4f}")
    console.print(
        f"Consensus scores  A={result.consensus_score_a:.4f}  B={result.consensus_score_b:.4f}"
    )
    console.print("Consensus universe:")
    for k, v in result.consensus_vector.items():
        console.print(f"  {k}: {v:.6g}")
    if out is not None:
        console.print(f"\nArtifacts written to: {out.resolve()}")


def main() -> None:
    app(prog_name="cosmogenesis")


if __name__ == "__main__":
    main()
