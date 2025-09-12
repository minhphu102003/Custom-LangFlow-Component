# Custom Components for Langflow

This repository contains custom components for Langflow that process DataFrames with text data using various processing strategies.

### Agent Component

The AgentComponent is a custom Langflow component that extends the base LCToolsAgentComponent to provide flexible agent functionality with tool calling capabilities. Key features include:

- **Multi-Provider Support**: Works with various LLM providers including Google Generative AI (Gemini), OpenAI, Anthropic, and Groq
- **Tool Integration**: Can integrate with MCP (Model Coordination Protocol) servers for enhanced tool calling
- **Customizable Prompts**: Allows setting system prompts to guide agent behavior
- **Date Tool**: Optional current date tool for time-aware responses
- **Flexible Configuration**: Supports various model configurations and parameters

**Usage Example**:

```python
from processors.agent_component import AgentComponent
from langflow.schema.message import Message

agent = AgentComponent()
agent.system_prompt = "You are a helpful AI assistant."
agent.input_value = Message(text="Explain quantum computing.")
agent.agent_llm = "Google Generative AI"
agent.model_name = "gemini-2.0-flash-001"
agent.add_current_date_tool = True

# Run the agent
response = await agent.message_response()
```

### Parallel Agent Processor

The ParallelAgentProcessor is designed to process multiple queries simultaneously by creating individual AgentComponent instances for each query. Key features include:

- **Dynamic Worker Allocation**: Automatically determines optimal number of workers based on DataFrame size
- **Parallel Processing**: Uses ThreadPoolExecutor for concurrent processing of multiple queries
- **MCP Server Integration**: Can connect to MCP servers to provide tools to all agents
- **Flexible Configuration**: Supports custom system prompts and model configurations
- **Result Aggregation**: Combines results from all agents into structured or string formats

**How It Works**:

1. Takes a DataFrame with a "text" column as input
2. Dynamically creates AgentComponent instances based on the number of records
3. Processes each record in parallel using separate agents
4. Aggregates results into a combined output

**Usage Example**:

```python
from processors.parallel_agent_processor import ParallelAgentProcessor

processor = ParallelAgentProcessor()
processor.dataframe_input = {
    "data": [
        {"text": "Explain artificial intelligence."},
        {"text": "What is machine learning?"},
        {"text": "How do neural networks work?"}
    ]
}
processor.system_prompt = "You are a helpful AI assistant."
processor.agent_llm = "Google Generative AI"
processor.model_name = "gemini-2.0-flash-001"

# Process all queries in parallel
results = processor.build_processed_results()
detailed_results = processor.build_detailed_results()
```

## Project Structure

```
custom_components/
├── processors/          # Main processor components
│   ├── agent_component.py         # Individual agent component
│   ├── parallel_agent_processor.py # Parallel processing component
│   ├── base_processor.py          # Base class for processors
├── utils/               # Utility functions and modules
│   ├── utils.py                   # General utility functions
│   ├── result_processing.py       # Result formatting functions
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

For detailed information about the components and usage, refer to the source code and test files:

- Review the source code in the `processors/` directory
- Check the test files in the `tests/` directory for usage examples
- Examine the utility functions in the `utils/` directory

## Testing

Run the test scripts to verify functionality:

```bash
cd tests
python test_all_components.py
python verify_installation.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
