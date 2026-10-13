.PHONY: test-install venv

VENV = .venv
ifeq ($(OS),Windows_NT)
    PYTHON = $(VENV)/bin/python.exe
    PIP = $(VENV)/bin/pip.exe
else
    PYTHON = $(VENV)/bin/python
    PIP = $(VENV)/bin/pip
endif

venv:
	python3 -m venv $(VENV)
	
test-install: venv
	$(PIP) install pytest pytest-cov

test-cor: venv  test-install
	$(PYTHON) -m pytest tests/test_stack_machine.py tests/test_main_cli.py --cov=plib --cov-report=term-missing --cov-branch

run: venv
	$(PYTHON) plib/main.py "${EXP}"

help: venv
	$(PYTHON) plib/main.py -h
