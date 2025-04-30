# Values in the Wild: Implementation and Analysis Framework

A comprehensive toolkit for implementing, analyzing, and validating AI value alignment based on Anthropic's "Values in the Wild" research.

## Architecture

```mermaid
graph TD
    subgraph Core["Core Framework"]
        Extract[Extraction Module]
        Taxonomy[Taxonomy Module]
        Anon[Anonymization Module]
        Simulate[Simulation Module]
        Analyze[Analysis Module]
    end

    subgraph Data["Data Resources"]
        ValueData[Value Taxonomies]
        Samples[Chat Samples]
        Frequencies[Value Frequencies]
    end

    subgraph Workflows["Workflows"]
        Extract_Flow[Value Extraction]
        Analysis_Flow[Distribution Analysis] 
        Simulation_Flow[Chat Simulation]
        Anonymization_Flow[Privacy-Preserving Anonymization]
    end

    %% Core Module Relationships
    Extract --> Taxonomy
    Simulate --> Taxonomy
    Analyze --> Taxonomy
    
    %% Data Relationships
    ValueData --> Taxonomy
    Frequencies --> Simulate
    Samples --> Extract
    Extract --> Samples
    
    %% Workflow Relationships
    Extract_Flow --> Extract
    Extract_Flow --> Anon
    Analysis_Flow --> Analyze
    Simulation_Flow --> Simulate
    Anonymization_Flow --> Anon
    
    %% Privacy Layer
    Anon -.-> Extract
    Anon -.-> Analyze
    
    classDef core fill:#f9f,stroke:#333,stroke-width:2px
    classDef data fill:#bbf,stroke:#333,stroke-width:1px
    classDef flow fill:#bfb,stroke:#333,stroke-width:1px
    
    class Extract,Taxonomy,Anon,Simulate,Analyze core
    class ValueData,Samples,Frequencies data
    class Extract_Flow,Analysis_Flow,Simulation_Flow,Anonymization_Flow flow
```

## Environment Setup

This project uses `uv` for Python dependency management and `make` for workflow automation.

### Prerequisites

- Python 3.9+
- uv (Python package manager)
- Make

### Setup Workflow

```mermaid
sequenceDiagram
    participant User
    participant Make
    participant UV
    participant Python
    
    User->>Make: make setup
    Make->>UV: uv venv .venv
    UV-->>Make: Virtual environment created
    Make->>UV: uv pip install -r requirements.txt
    UV-->>Make: Dependencies installed
    Make-->>User: Setup complete
    
    User->>Make: make activate
    Make-->>User: Environment activation instructions
    
    User->>Make: make download-all
    Make->>Python: Download papers and datasets
    Python-->>Make: Downloads complete
    Make-->>User: Resources ready
```

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/defrecord/value-alignment-toolkit.git
   cd value-alignment-toolkit
   ```

2. **Set up the environment:**
   ```bash
   make setup
   ```
   This will create a virtual environment using uv and install all dependencies.

3. **Activate the environment:**
   ```bash
   source .venv/bin/activate  # or use 'make activate' for instructions
   ```

4. **Download required resources:**
   ```bash
   make download-all
   ```

5. **Run a sample analysis:**
   ```bash
   make sample-analysis
   ```

## Project Structure

- `src/`: Core implementation modules
  - `extraction/`: Value extraction algorithms
  - `simulation/`: Chat system simulation
  - `anonymization/`: Privacy-preserving techniques
  - `analysis/`: Statistical tools and visualizations
  - `taxonomy/`: Value hierarchy implementation

- `data/`: Data resources and outputs
  - `values/`: Reference data including value frequencies and taxonomies
  - `samples/`: Generated and anonymized conversation datasets

- `tools/`: Utility scripts
  - `download/`: Scripts to fetch relevant research papers and resources
  - `validation/`: Tools for testing and validating the implementation

- `docs/`: Documentation
  - `tutorials/`: Implementation guides and usage examples
  - `paper/`: Summaries of research methodology and key findings

## Available Commands

Run `make help` to see all available commands.

## License

[Appropriate license information]

## Acknowledgments

This work builds upon research by Anthropic's "Values in the Wild" paper authored by Saffron Huang, Esin Durmus, et al.