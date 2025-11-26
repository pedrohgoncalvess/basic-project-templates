PYTHON_PATH ?=
VENV = .venv
UV_INSTALLER = uv-installer-latest.exe
UV_DOWNLOAD_URL = https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.exe
PYTHON_VERSION_FILE = .python-version

ifeq ($(OS),Windows_NT)
    RM = rmdir /s /q
    PYTHON_DEFAULT = python
    PIP = $(VENV)\Scripts\pip
    PYTHON_VENV = $(VENV)\Scripts\python
    UV = uv.exe
    NULL_OUTPUT = >nul 2>&1
    WHICH = where
    SHELL := cmd.exe
    .SHELLFLAGS := /c
else
    RM = rm -rf
    PYTHON_DEFAULT = python3
    PIP = $(VENV)/bin/pip
    PYTHON_VENV = $(VENV)/bin/python
    UV ?= $(HOME)/.local/bin/uv
    NULL_OUTPUT = >/dev/null 2>&1
    WHICH = which
    SHELL := /bin/bash
endif

.PHONY: setup run clean check-uv install-uv check-python-version install-python create-venv install-deps

check-uv:
	@echo Checking UV installation...
ifeq ($(OS),Windows_NT)
	@$(WHICH) uv $(NULL_OUTPUT) || (echo UV not found. Installing... && $(MAKE) install-uv)
else
	@command -v uv $(NULL_OUTPUT) || command -v $(UV) $(NULL_OUTPUT) || \
		(echo "UV not found. Installing..." && $(MAKE) install-uv)
endif

install-uv:
	@echo Installing UV...
ifeq ($(OS),Windows_NT)
	@echo Downloading UV installer...
	@powershell -Command "Invoke-WebRequest -Uri '$(UV_DOWNLOAD_URL)' -OutFile '$(UV_INSTALLER)'"
	@echo Installing UV...
	@$(UV_INSTALLER)
	@del $(UV_INSTALLER)
else
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo 'export PATH="$$HOME/.local/bin:$$PATH"' >> ~/.bashrc 2>/dev/null || true
	@echo 'export PATH="$$HOME/.local/bin:$$PATH"' >> ~/.zshrc 2>/dev/null || true
endif
	@echo UV successfully installed!

check-python-version: check-uv
	@echo Checking Python version requirements...
ifeq ($(OS),Windows_NT)
	@if exist $(PYTHON_VERSION_FILE) ( \
		for /f %%i in ($(PYTHON_VERSION_FILE)) do set REQUIRED_VERSION=%%i && \
		echo Required Python version: %%i && \
		$(UV) python list | findstr %%i $(NULL_OUTPUT) || ( \
			echo Python %%i not found. Installing... && $(MAKE) install-python \
		) \
	) else ( \
		echo No $(PYTHON_VERSION_FILE) found. Using default Python. \
	)
else
	@if [ -f $(PYTHON_VERSION_FILE) ]; then \
		REQUIRED_VERSION=$$(cat $(PYTHON_VERSION_FILE)); \
		echo "Required Python version: $$REQUIRED_VERSION"; \
		$(UV) python list | grep -q "$$REQUIRED_VERSION" || { \
			echo "Python $$REQUIRED_VERSION not found. Installing..."; \
			$(MAKE) install-python; \
		}; \
	else \
		echo "No $(PYTHON_VERSION_FILE) found. Using default Python."; \
	fi
endif

install-python: check-uv
	@echo Installing required Python version...
ifeq ($(OS),Windows_NT)
	@for /f %%i in ($(PYTHON_VERSION_FILE)) do $(UV) python install %%i
else
	@if [ -f $(PYTHON_VERSION_FILE) ]; then \
		REQUIRED_VERSION=$$(cat $(PYTHON_VERSION_FILE)); \
		$(UV) python install $$REQUIRED_VERSION; \
	else \
		echo "ERROR: $(PYTHON_VERSION_FILE) not found!"; \
		exit 1; \
	fi
endif
	@echo Python installed successfully!

create-venv: check-python-version
	@echo Checking if virtual environment exists...
ifeq ($(OS),Windows_NT)
	@if exist $(VENV) $(RM) $(VENV) $(NULL_OUTPUT)
	@echo Creating virtual environment...
	@if not "$(PYTHON_PATH)"=="" ( \
		if exist "$(PYTHON_PATH)" ( \
			echo Using provided Python path: $(PYTHON_PATH) && \
			$(UV) venv $(VENV) --python "$(PYTHON_PATH)" --link-mode=copy \
		) else ( \
			echo ERROR: PYTHON_PATH not found! && exit 1 \
		) \
	) else if exist $(PYTHON_VERSION_FILE) ( \
		for /f %%i in ($(PYTHON_VERSION_FILE)) do ( \
			echo Using Python version from $(PYTHON_VERSION_FILE): %%i && \
			$(UV) venv $(VENV) --python %%i --link-mode=copy \
		) \
	) else ( \
		echo Creating virtual environment with default Python... && \
		$(UV) venv $(VENV) --link-mode=copy \
	)
else
	@if [ -d $(VENV) ]; then $(RM) $(VENV); fi
	@echo "Creating virtual environment..."
	@if [ -n "$(PYTHON_PATH)" ]; then \
		if [ -x "$(PYTHON_PATH)" ]; then \
			echo "Using provided Python path: $(PYTHON_PATH)"; \
			$(UV) venv $(VENV) --python "$(PYTHON_PATH)" --link-mode=copy; \
		else \
			echo "ERROR: PYTHON_PATH not found or not executable!"; \
			exit 1; \
		fi; \
	elif [ -f $(PYTHON_VERSION_FILE) ]; then \
		REQUIRED_VERSION=$$(cat $(PYTHON_VERSION_FILE)); \
		echo "Using Python version from $(PYTHON_VERSION_FILE): $$REQUIRED_VERSION"; \
		$(UV) venv $(VENV) --python "$$REQUIRED_VERSION" --link-mode=copy; \
	else \
		echo "Creating virtual environment with default Python..."; \
		$(UV) venv $(VENV) --link-mode=copy; \
	fi
endif
	@echo Virtual environment created successfully!

install-deps: create-venv
	@echo Installing dependencies...
ifeq ($(OS),Windows_NT)
	@if exist requirements.txt ( \
		echo Installing from requirements.txt... && \
		$(UV) pip install -r requirements.txt --link-mode=copy \
	) else if exist pyproject.toml ( \
		echo Installing from pyproject.toml... && \
		$(UV) sync --link-mode=copy \
	) else ( \
		echo No requirements.txt or pyproject.toml found. Skipping dependency installation. \
	)
else
	@if [ -f requirements.txt ]; then \
		echo "Installing from requirements.txt..."; \
		$(UV) pip install -r requirements.txt --link-mode=copy; \
	elif [ -f pyproject.toml ]; then \
		echo "Installing from pyproject.toml..."; \
		$(UV) sync --link-mode=copy; \
	else \
		echo "No requirements.txt or pyproject.toml found. Skipping dependency installation."; \
	fi
endif
	@echo Dependencies installed successfully!

setup: install-deps
	@echo Setup completed successfully!

run:
	@$(PYTHON_VENV) main.py

clean:
ifeq ($(OS),Windows_NT)
	@if exist $(VENV) $(RM) $(VENV)
else
	@$(RM) $(VENV)
endif
	@echo Virtual environment removed!

help:
	@echo Available targets:
	@echo   setup              - Complete setup (install UV, Python, create venv, install deps)
	@echo   run                - Run main.py
	@echo   clean              - Remove virtual environment
	@echo   check-uv           - Check if UV is installed
	@echo   install-uv         - Install UV package manager
	@echo   check-python-version - Check if required Python version is available
	@echo   install-python     - Install Python version from .python-version
	@echo   create-venv        - Create virtual environment
	@echo   install-deps       - Install project dependencies
	@echo.
	@echo Usage:
	@echo   make setup                    - Setup with auto-detected Python
	@echo   make setup PYTHON_PATH=path   - Setup with specific Python executable