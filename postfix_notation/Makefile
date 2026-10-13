VENV = .venv

ifeq ($(OS),Windows_NT)
    PYTHON = $(VENV)\Scripts\python.exe
    PIP    = $(VENV)\Scripts\pip.exe
    VENV_PY = python
else
    PYTHON = $(VENV)/bin/python
    PIP    = $(VENV)/bin/pip
    VENV_PY = python3
endif

$(PYTHON):
	$(VENV_PY) -m venv $(VENV)

venv: $(PYTHON)

test-install: $(PYTHON)
	$(PIP) install pytest pytest-cov

test-cor: $(PYTHON) test-install
	$(PYTHON) -m pytest tests/test_stack_machine.py tests/test_main_cli.py --cov=plib --cov-report=term-missing --cov-branch

run: $(PYTHON)
	$(PYTHON) plib/main.py "${EXP}"

help: $(PYTHON)
	$(PYTHON) plib/main.py -h