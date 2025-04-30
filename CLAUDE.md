# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Note: While this file is machine-generated, it should NOT be marked as "generated" in .gitattributes. It serves as a crucial interface between humans and AI assistants, and merging conflicts should be resolved manually to ensure accurate guidance.

## Build/Test/Lint Commands
- **Environment**: Use `make setup` to create a virtual environment with uv, then `make activate` for instructions
- **Python**: Use `make test` to run all tests or `uv run python -m pytest tests/test_file.py::test_function` for single tests
- **Linting**: Use `make lint` to run flake8 and mypy, or `make format` to run Black
- **Documentation**: Use `make docs` to generate API documentation
- **Sample Analysis**: Use `make sample-analysis` for a quick demo of the toolkit's capabilities
- **Simulation**: Use `make simulate` to run a value-based chat simulation

## Code Style Guidelines
- **Python**: Follow PEP 8 conventions with Black formatting (line length: 88)
- **Imports**: Group by stdlib → third-party → local with one blank line separating groups
- **Types**: Use type annotations for all function parameters and return values
- **Naming**: `snake_case` for variables/functions, `PascalCase` for classes, `UPPER_CASE` for constants
- **Error Handling**: Use specific exceptions with informative messages; prefer context managers
- **Documentation**: Google-style docstrings with parameters, returns, and examples
- **Privacy**: Never log or store sensitive information; always use anonymization functions
- **Testing**: Write unit tests for all new functionality, including edge cases and error paths