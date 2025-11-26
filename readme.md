# Python Project Generator

## Overview

This Python Project Generator is a command-line tool that helps you quickly create Python project structures using predefined templates. It supports multiple project templates including default, API, ETL, and Machine Learning/Analytics projects.

## Prerequisites

- Python 3.10+
- uv

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/pedrohgoncalvess/template-generator.git
cd template-generator
```

### 2. Create Virtual Environment and install necessary packages

```bash
uv init
uv sync
```
or using pip
```
pip -m venv .venv
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

# Specify a custom set of files
npt --name my-project --custom custom.example.yaml
```

### Available Templates

- `default`: Standard Python project structure.
- `api`: FAST API project structure.
- `etl-airflow`: Data engineering project structure with Airflow.
- `etl-prefect`: Data engineering project structure with Prefect.
- `ml`: Machine Learning and Analytics project template.

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

### ML Template
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
git clone https://github.com/pedrohgoncalvess/basic-project-templates
cd project-generator

# Create virtual environment
uv init

# Install development dependencies
uv pip install -e .
```

## Running Tests

```bash
# Run tests
pytest tests/
```

## License

[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html)

## Support

If you encounter any problems, please [file an issue](https://github.com/pedrohgoncalvess/template-generator/issues) on GitHub.
