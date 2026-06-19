.PHONY: install test lint demo clean

install:
	python -m pip install -e .[dev]

test:
	PYTHONPATH=src pytest

lint:
	ruff check src tests

demo:
	PYTHONPATH=src python -m quantaengine run --config examples/minimal_universe.yaml --out runs/demo --steps 128 --snapshot-every 16 --plot

clean:
	rm -rf runs outputs build dist *.egg-info .pytest_cache .ruff_cache .mypy_cache
