# Python Project Generator

## Overview

This Python Project Generator is a command-line tool that helps you quickly create Python project structures using predefined templates. It supports multiple project templates including default, API, ETL, and Machine Learning/Analytics projects.

## Prerequisites

- Python 3.9+
- pip
- virtualenv (recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/project-generator.git
cd project-generator
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the Package

```bash
pip install -e .
```

## Usage

### Generate a Project

```bash
# Basic usage
npt --name my-project

# Specify a template
npt --name my-api-project --template api

# Specify a custom path
npt --name my-project --path /path/to/projects
```

### Available Templates

- `default`: Standard Python project structure
- `api`: API-focused project setup
- `etl`: Extract, Transform, Load project structure
- `analytics-ml`: Machine Learning and Analytics project template

## Example

```bash
# Create a new API project
npt --name my-awesome-api --template api
```

## Project Templates Details

### Default Template
- Basic Python project structure
- Includes README, .gitignore
- Minimal configuration files

### API Template
- Flask/FastAPI ready structure
- Includes API routing
- Swagger/OpenAPI documentation setup

### ETL Template
- Data extraction and transformation setup
- Configuration for various data sources
- Logging and error handling

### Analytics-ML Template
- Machine Learning project structure
- Jupyter notebook integration
- Data preprocessing scripts
- Model training and evaluation templates

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/project-generator.git
cd project-generator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix
.venv\Scripts\activate     # On Windows

# Install development dependencies
pip install -e .
pip install -r requirements-dev.txt  # If you have dev requirements
```

## Running Tests

```bash
# Run tests
pytest tests/
```

## License

[Specify your license, e.g., MIT]

## Support

If you encounter any problems, please [file an issue](https://github.com/pedrohgoncalvess/template-generator/issues) on GitHub.