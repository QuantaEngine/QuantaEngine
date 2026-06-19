# Contributing to QuantaEngine

QuantaEngine welcomes contributions in three categories:

1. **Physics modules**: new equations, field types, validation tests, benchmark comparisons.
2. **Numerics**: better integrators, performance, GPU backends, stability checks.
3. **User experience**: examples, docs, visualization, CLI improvements.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
ruff check .
```

## Contribution rule

Do not claim physical validity without tests, references, or benchmark comparisons. A toy model is welcome when it is clearly labeled as a toy model.
