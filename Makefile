.PHONY: test validate demo check
PYTHON ?= python3

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

validate:
	PYTHONPATH=src $(PYTHON) -m kompose.cli validate examples/capsule-rivieres

demo:
	PYTHONPATH=src $(PYTHON) -m kompose.cli demo-flow examples/capsule-rivieres

check: test validate demo
