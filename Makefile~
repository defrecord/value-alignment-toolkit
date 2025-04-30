# Makefile for Value Alignment Toolkit

.PHONY: all setup test clean docs lint format

# Default target
all: setup test

# Setup development environment
setup:
	@echo "Setting up development environment..."
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "Setup complete. Activate with: source venv/bin/activate"

# Run tests
test:
	@echo "Running tests..."
	python -m pytest tests/

# Run tests with coverage
coverage:
	@echo "Running tests with coverage..."
	python -m pytest --cov=src tests/
	python -m pytest --cov=src --cov-report=html tests/

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf __pycache__/
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete

# Generate documentation
docs:
	@echo "Generating documentation..."
	mkdir -p docs/api
	pdoc --html --output-dir docs/api src/

# Lint code
lint:
	@echo "Linting code..."
	flake8 src/ tests/
	mypy src/

# Format code
format:
	@echo "Formatting code..."
	black src/ tests/

# Download research papers
download-papers:
	@echo "Downloading research papers..."
	bash tools/download/download_papers.sh

# Generate sample data
generate-samples:
	@echo "Generating sample data..."
	python tools/validation/generate_sample_data.py

# Run simulation
simulate:
	@echo "Running simulation..."
	python -c "from src.simulation.chat_simulator import ChatSimulator; simulator = ChatSimulator(); results = simulator.run_simulation(); print(f\"Simulation complete with {results['summary']['message_count']} messages\")"

# Help
help:
	@echo "Available targets:"
	@echo "  all              : Setup environment and run tests"
	@echo "  setup            : Set up development environment"
	@echo "  test             : Run tests"
	@echo "  coverage         : Run tests with coverage reporting"
	@echo "  clean            : Clean build artifacts"
	@echo "  docs             : Generate documentation"
	@echo "  lint             : Lint code"
	@echo "  format           : Format code"
	@echo "  download-papers  : Download research papers"
	@echo "  generate-samples : Generate sample data files"
	@echo "  simulate         : Run a simple simulation"
	@echo "  help             : Show this help message"
