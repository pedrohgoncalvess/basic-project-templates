PYTHON_VERSION ?= 3.12.6
PYTHON_PATH ?=        # Optional: ex. /usr/local/bin/python3.13t
VENV = .venv
UV_INSTALLER = uv-installer-latest.exe

ifeq ($(OS),Windows_NT)
    PYTHON_DEFAULT = python
    PIP = $(VENV)\Scripts\pip
    PYTHON_VENV = $(VENV)\Scripts\python
    UV = uv.exe
    NULL_OUTPUT = >nul 2>&1
    UV_DOWNLOAD_URL = https://uv.wtf/releases/latest/windows/$(UV_INSTALLER)
    EXPORT_ENV = set UV_LINK_MODE=copy&&
else
    PYTHON_DEFAULT = python3
    PIP = $(VENV)/bin/pip
    PYTHON_VENV = $(VENV)/bin/python
    UV = uv
    NULL_OUTPUT = >/dev/null 2>&1
    UV_DOWNLOAD_URL = https://uv.wtf/releases/latest/linux/uv
    EXPORT_ENV = UV_LINK_MODE=copy
endif

.PHONY: setup run clean check-uv install-uv check-python create-venv install-deps

check-uv:
	@echo Checking UV installation...
ifeq ($(OS),Windows_NT)
	@where $(UV) $(NULL_OUTPUT) || (echo UV not found. Installing... && $(MAKE) install-uv)
else
	@which $(UV) $(NULL_OUTPUT) || (echo UV not found. Installing... && $(MAKE) install-uv)
endif

install-uv:
	@echo Downloading UV installer...
ifeq ($(OS),Windows_NT)
	@curl -Lo $(UV_INSTALLER) $(UV_DOWNLOAD_URL)
	@echo Installing UV...
	@$(UV_INSTALLER) /quiet
	@del $(UV_INSTALLER)
else
	@curl -Lo $(UV) $(UV_DOWNLOAD_URL)
	@chmod +x $(UV)
	@mv $(UV) /usr/local/bin/
endif
	@echo UV successfully installed!

check-python:
	@echo Checking Python...
ifeq ($(strip $(PYTHON_PATH)),)
	@if ! command -v $(PYTHON_DEFAULT) $(NULL_OUTPUT); then \
		echo "$(PYTHON_DEFAULT) not found. Will use UV to install Python $(PYTHON_VERSION)."; \
	else \
		echo "Found Python: $$($(PYTHON_DEFAULT) --version)"; \
	fi
else
	@if [ ! -x "$(PYTHON_PATH)" ]; then \
		echo "ERROR: Provided PYTHON_PATH '$(PYTHON_PATH)' not found or not executable."; \
		exit 1; \
	else \
		echo "Using provided Python path: $(PYTHON_PATH)"; \
		"$(PYTHON_PATH)" --version; \
	fi
endif

create-venv: check-uv check-python
	@echo Checking if virtual environment exists...
ifeq ($(OS),Windows_NT)
	@if exist $(VENV) ( \
		echo Virtual environment already exists. Recreating... && \
		rmdir /s /q $(VENV) \
	)
else
	@if [ -d $(VENV) ]; then \
		echo Virtual environment already exists. Recreating... && \
		rm -rf $(VENV); \
	fi
endif
	@echo Creating new virtual environment with UV...
ifeq ($(strip $(PYTHON_PATH)),)
	@if command -v $(PYTHON_DEFAULT) $(NULL_OUTPUT); then \
		$(UV) venv $(VENV) --python $(PYTHON_DEFAULT) --link-mode=copy; \
	else \
		$(UV) venv $(VENV) --python $(PYTHON_VERSION) --link-mode=copy; \
	fi
else
	@$(UV) venv $(VENV) --python $(PYTHON_PATH) --link-mode=copy
endif
	@echo Virtual environment successfully created!

install-deps: create-venv
	@echo Checking for requirements.txt...
ifeq ($(OS),Windows_NT)
	@if exist requirements.txt ( \
		echo Installing dependencies from requirements.txt... && \
		$(UV) pip install -r requirements.txt --link-mode=copy \
	) else ( \
		echo No requirements.txt found. Using UV sync... && \
		$(UV) sync --link-mode=copy \
	)
else
	@if [ -f requirements.txt ]; then \
		echo Installing dependencies from requirements.txt... && \
		$(EXPORT_ENV) $(UV) pip install -r requirements.txt; \
	else \
		echo No requirements.txt found. Using UV sync... && \
		$(EXPORT_ENV) $(UV) sync --link-mode=copy; \
	fi
endif
	@echo Dependencies installed successfully!

setup: install-deps
	@echo Setup completed!

clean:
ifeq ($(OS),Windows_NT)
	@if exist $(VENV) rmdir /s /q $(VENV)
else
	@rm -rf $(VENV)
endif
