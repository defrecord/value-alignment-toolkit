# Makefile for Value Alignment Toolkit
.PHONY: all setup test clean docs lint format download-papers download-data download-all activate sample-analysis .init

# Python commands using uv
PYTHON := uv run python
PIP := uv pip
VENV_DIR := .venv

# Default target
all: setup test

# Check if virtual environment exists
.init:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@touch .init

# Setup development environment
setup:
	@echo "Setting up development environment with uv..."
	@command -v uv >/dev/null 2>&1 || { echo "uv is not installed. Install with 'pip install uv'."; exit 1; }
	uv venv $(VENV_DIR)
	$(PIP) install -r requirements.txt
	@touch .init
	@echo "Setup complete. Run 'make activate' for activation instructions."

# Display activation instructions
activate:
	@echo "To activate the environment, run:"
	@echo "source $(VENV_DIR)/bin/activate"
	@echo
	@echo "For fish shell:"
	@echo "source $(VENV_DIR)/bin/activate.fish"
	@echo
	@echo "For csh/tcsh:"
	@echo "source $(VENV_DIR)/bin/activate.csh"

# Run tests
test: .init
	@echo "Running tests..."
	$(PYTHON) -m pytest tests/

# Run tests with coverage
coverage: .init
	@echo "Running tests with coverage..."
	$(PYTHON) -m pytest --cov=src tests/
	$(PYTHON) -m pytest --cov=src --cov-report=html tests/

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -f .init
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete

# Deep clean (including virtual environment)
deepclean: clean
	@echo "Removing virtual environment..."
	rm -rf $(VENV_DIR)

# Generate documentation
docs: .init
	@echo "Generating documentation..."
	mkdir -p docs/api
	$(PYTHON) -m pdoc --html --output-dir docs/api src/

# Lint code
lint: .init
	@echo "Linting code..."
	$(PYTHON) -m flake8 src/ tests/
	$(PYTHON) -m mypy src/

# Format code
format: .init
	@echo "Formatting code..."
	$(PYTHON) -m black src/ tests/

# Download research papers
download-papers:
	@echo "Downloading research papers..."
	bash scripts/download_papers.sh

# Download Values in the Wild dataset
download-data:
	@echo "Downloading Values in the Wild dataset..."
	bash scripts/download_hf_vitw.sh

# Download all resources (papers and datasets)
download-all: download-papers download-data
	@echo "All downloads complete."

# Generate sample data
generate-samples: .init
	@echo "Generating sample data..."
	$(PYTHON) tools/validation/generate_sample_data.py

# Run simulation
simulate: .init
	@echo "Running simulation..."
	$(PYTHON) -c "from src.simulation.chat_simulator import ChatSimulator; simulator = ChatSimulator(); results = simulator.run_simulation(); print(f\"Simulation complete with {results['summary']['message_count']} messages\")"

# Run a sample analysis (useful for new users)
sample-analysis: .init download-all
	@echo "Running sample analysis..."
	$(PYTHON) -c "from src.analysis.value_analyzer import ValueAnalyzer; analyzer = ValueAnalyzer(); analyzer.run_sample_analysis()"

# Help
help:
	@echo "Available targets:"
	@echo "  all              : Setup environment and run tests"
	@echo "  setup            : Set up development environment using uv"
	@echo "  activate         : Show environment activation instructions"
	@echo "  test             : Run tests"
	@echo "  coverage         : Run tests with coverage reporting"
	@echo "  clean            : Clean build artifacts"
	@echo "  deepclean        : Clean build artifacts and remove virtual environment"
	@echo "  docs             : Generate documentation"
	@echo "  lint             : Lint code"
	@echo "  format           : Format code"
	@echo "  download-papers  : Download research papers to .cache/"
	@echo "  download-data    : Download Values in the Wild dataset to data/"
	@echo "  download-all     : Download both papers and dataset"
	@echo "  generate-samples : Generate sample data files"
	@echo "  simulate         : Run a simple simulation"
	@echo "  sample-analysis  : Run a sample analysis workflow (good starting point)"
	@echo "  help             : Show this help message"