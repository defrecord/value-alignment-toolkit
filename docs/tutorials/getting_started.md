# Getting Started with Value Alignment Toolkit

This tutorial will guide you through setting up and using the Value Alignment Toolkit for analyzing and simulating value expressions in AI systems.

## Prerequisites

- Python 3.8+
- pip or conda
- Optional: Guile 3.0+ (for advanced simulation features)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aygp-dr/value-alignment-toolkit.git
   cd value-alignment-toolkit
   ```

2. Set up a virtual environment:
   ```bash
   # Create the virtual environment
   python -m venv venv
   
   # Activate the environment (Linux/macOS)
   source venv/bin/activate
   
   # Activate the environment (Windows)
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   ```

## Basic Usage

### 1. Downloading Research Papers

The toolkit includes a script to download relevant research papers:

```bash
# Run the downloader script
bash tools/download/download_papers.sh
```

This will download papers to the `.cache` directory.

### 2. Running a Chat Simulation

To run a basic chat simulation:

```python
from src.simulation.chat_simulator import ChatSimulator

# Create and run a simulation
simulator = ChatSimulator()
results = simulator.run_simulation(num_users=10, chats_per_user=5, messages_per_chat=10)

print(f"Simulation complete with {results['summary']['message_count']} messages")
```

### 3. Extracting Values

To extract values from conversation data:

```python
from src.extraction.extractor import ValueExtractor

# Create a value extractor
extractor = ValueExtractor()

# Extract values from a text
sample_text = "I'm here to help you understand this concept with clarity and transparency."
values = extractor.extract_from_text(sample_text)

print(f"Extracted values: {values}")
```

### 4. Anonymizing Data

To anonymize data for privacy-preserving analysis:

```python
from src.anonymization.anonymizer import Anonymizer
from datetime import datetime

# Create an anonymizer
anonymizer = Anonymizer()

# Anonymize a sample user
user_data = {
    "id": 123,
    "username": "johndoe",
    "demographics": {
        "age": 34,
        "location": "San Francisco"
    },
    "chats": [1, 2, 3],
    "values": ["privacy", "honesty"]
}

anon_user = anonymizer.anonymize_user(user_data)
print(f"Anonymized user: {anon_user}")
```

## Next Steps

- Explore the [documentation](../README.md) for more details on each module
- Check out the [examples](../data/samples) for sample data and usage patterns
- Read about the [research foundation](../docs/paper/summary.md) behind the toolkit

For more detailed tutorials, see the [tutorials directory](../docs/tutorials).
