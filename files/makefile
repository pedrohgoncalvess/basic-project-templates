PYTHON_VERSION = 3.11.0
VENV = .venv

ifeq ($(OS),Windows_NT)
    PYTHON = python
    PIP = $(VENV)\Scripts\pip
    PYTHON_VENV = $(VENV)\Scripts\python
    NULL_OUTPUT = >nul 2>&1
    PYTHON_INSTALLER = python-$(PYTHON_VERSION)-amd64.exe
    DOWNLOAD_URL = https://www.python.org/ftp/python/$(PYTHON_VERSION)/$(PYTHON_INSTALLER)
else
    PYTHON = python3
    PIP = $(VENV)/bin/pip
    PYTHON_VENV = $(VENV)/bin/python
    NULL_OUTPUT = >/dev/null 2>&1
endif

.PHONY: setup run clean check-python install-python create-venv

check-python:
	@echo Checking Python installation...
ifeq ($(OS),Windows_NT)
	@where python $(NULL_OUTPUT) || (echo Python not found. Installing... && $(MAKE) install-python)
else
	@which python3 $(NULL_OUTPUT) || (echo Python not found. Please install Python $(PYTHON_VERSION))
endif

install-python:
ifeq ($(OS),Windows_NT)
	@echo Downloading Python $(PYTHON_VERSION)
	@certutil -urlcache -f $(DOWNLOAD_URL) $(PYTHON_INSTALLER)
	@echo Installing Python $(PYTHON_VERSION)
	@$(PYTHON_INSTALLER) /quiet InstallAllUsers=1 PrependPath=1 DefaultJustForMe=0
	@echo Cleaning installer
	@del $(PYTHON_INSTALLER)
	@echo Python successfully installed
	@timeout /t 5 /nobreak $(NULL_OUTPUT)
else
	@echo Please install Python $(PYTHON_VERSION) using your system's package manager:
	@echo For Ubuntu/Debian: sudo apt-get install python$(PYTHON_VERSION)
	@echo For MacOS: brew install python@$(PYTHON_VERSION)
	@exit 1
endif

create-venv:
	@echo Checking if virtual environment exists...
ifeq ($(OS),Windows_NT)
	@if exist $(VENV) (echo Virtual environment already exists. Skipping creation.) else ( \
		echo Creating new virtual environment... && \
		$(PYTHON) -m venv $(VENV) && \
		echo Checking pip... && \
		$(PYTHON_VENV) -m ensurepip --upgrade && \
		echo Updating pip... && \
		$(PYTHON_VENV) -m pip install --upgrade pip && \
		echo Virtual environment successfully created! \
	)
else
	@if [ -d $(VENV) ]; then \
		echo Virtual environment already exists. Skipping creation.; \
	else \
		echo Creating new virtual environment... && \
		$(PYTHON) -m venv $(VENV) && \
		echo Checking pip... && \
		$(PYTHON_VENV) -m ensurepip --upgrade && \
		echo Updating pip... && \
		$(PYTHON_VENV) -m pip install --upgrade pip && \
		echo Virtual environment successfully created!; \
	fi
endif

setup: check-python create-venv
	@echo Installing dependencies...
	@$(PIP) install -r requirements.txt
	@echo Setup completed!

run: setup
	@$(PYTHON_VENV) main.py

clean:
ifeq ($(OS),Windows_NT)
	@if exist $(VENV) rmdir /s /q $(VENV)
else
	@rm -rf $(VENV)
endif