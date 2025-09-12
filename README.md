# Custom Components for Langflow

This repository contains custom components for Langflow that process DataFrames with text data using various processing strategies.

## Components Overview

### 1. Simple DataFrame Processor

Processes DataFrame rows sequentially with agents that call tools to answer queries.

### 2. Parallel DataFrame Processor

Processes DataFrame rows in parallel, with each row processed by an agent that calls tools to answer queries.

### 3. Integrated Parallel Processor

Advanced processor that processes DataFrame rows in parallel with integrated tool calling capabilities.

### 4. Parallel Query Processor

Specialized processor for handling query processing in parallel.

### 5. Parallel Agent Processor

Processes DataFrame rows in parallel using multiple AgentComponent instances that can call MCP server tools via SSE. The number of workers is dynamically determined based on the number of records in the DataFrame.

## Project Structure

```
custom_components/
├── processors/          # Main processor components
├── utils/               # Utility functions and modules
└── tests/               # Test files and verification scripts
```

## Setup and Installation

1. Ensure you have Python 3.8+ and Langflow installed
2. Configure Langflow to recognize these custom components:
   ```bash
   langflow start --components-path /path/to/custom_components
   ```
3. Access Langflow at `http://localhost:7860`

## Documentation

- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Detailed folder structure
- [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md) - Complete setup and usage guide
- [EXAMPLE_FLOW.json](EXAMPLE_FLOW.json) - Example flow configuration

## Testing

Run the test scripts to verify functionality:

```bash
cd tests
python test_all_components.py
python verify_installation.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
