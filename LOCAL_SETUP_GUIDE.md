# Local Setup Guide for Custom Components in Langflow

This guide will help you set up and run the custom components in a local Langflow environment.

## Prerequisites

1. Python 3.8 or higher
2. Langflow installed
3. Git (optional, for version control)

## Installation Steps

### 1. Install Langflow

If you haven't already installed Langflow, you can do so using pip:

```bash
pip install langflow
```

### 2. Set up the Custom Components

1. Make sure your custom components are in the correct directory structure as described in PROJECT_STRUCTURE.md
2. The components should be in a directory that Langflow can access

### 3. Configure Langflow to Use Custom Components

Langflow needs to know where to find your custom components. You have a few options:

#### Option A: Place Components in Langflow's Custom Components Directory

1. Find your Langflow installation directory:

   ```bash
   pip show langflow
   ```

2. Navigate to the custom components directory (usually something like `langflow/custom_components/`)

3. Copy your entire `custom_components` folder to this directory

#### Option B: Use Environment Variable

1. Set the `LANGFLOW_COMPONENTS_PATH` environment variable to point to your custom components directory:

   On Windows:

   ```cmd
   set LANGFLOW_COMPONENTS_PATH=D:\AI\Test\custom_components
   ```

   On macOS/Linux:

   ```bash
   export LANGFLOW_COMPONENTS_PATH=/path/to/your/custom_components
   ```

#### Option C: Specify Path When Starting Langflow

You can also specify the path when starting Langflow:

```bash
langflow --components-path D:\AI\Test\custom_components
```

### 4. Start Langflow

Once you've configured the components path, start Langflow:

```bash
langflow start
```

Or if you want to specify the components path at startup:

```bash
langflow start --components-path D:\AI\Test\custom_components
```

## Using the Components in Langflow

### 1. Access the Langflow Interface

After starting Langflow, open your browser and go to:

```
http://localhost:7860
```

### 2. Create a New Flow

1. Click on "Create New Flow"
2. Give your flow a name
3. Click "Create"

### 3. Add Custom Components to Your Flow

1. In the flow editor, look for the "Components" panel on the left
2. You should see your custom components under their respective categories:

   - Simple DataFrame Processor
   - Parallel DataFrame Processor
   - Integrated Parallel Processor
   - Parallel Query Processor
   - Parallel Agent Processor

3. Drag and drop the components you want to use onto the canvas

### 4. Connect and Configure Components

1. Connect components by dragging from one component's output to another's input
2. Click on each component to configure its parameters:
   - DataFrame Input: Provide your data in the expected format
   - Agent Prompt Template: Customize the prompt for your agents
   - Max Workers: Set the number of parallel workers (for parallel processors)
   - Agent Count: Set the number of agents to use per query (for Parallel Agent Processor)
   - MCP Server: Connect an MCP server for tool access (for components that support it)

### 5. Run Your Flow

1. Click the "Play" button to run your flow
2. Monitor the execution in the logs panel
3. View results in the output components

## Example Usage

Here's a simple example of how to use the components:

### Simple DataFrame Processing

1. Add a "Simple DataFrame Processor" component
2. Configure the DataFrame Input with data like:
   ```json
   {
     "data": [
       { "text": "What is artificial intelligence?" },
       { "text": "How does machine learning work?" },
       { "text": "What are neural networks?" }
     ]
   }
   ```
3. Connect the "Processed Results" output to a display component or file writer

### Parallel Processing

1. Add a "Parallel DataFrame Processor" component
2. Configure with the same data format as above
3. Set Max Workers to control parallelization (e.g., "4")
4. Connect outputs as needed

### Parallel Agent Processing with MCP Server

1. Add a "Parallel Agent Processor" component
2. Configure with your data
3. Set Max Workers to control parallelization (e.g., "4")
4. Set Agent Count to control how many agents process each query (e.g., "3")
5. Connect an MCP Server component to the MCP Server input
6. Connect outputs as needed

## Troubleshooting

### Common Issues

1. **Components Not Appearing**:

   - Check that the components path is correctly set
   - Verify that your `__init__.py` files are properly configured
   - Restart Langflow after making changes

2. **Import Errors**:

   - Ensure all dependencies are installed
   - Check that the Langflow version is compatible
   - Verify Python path settings

3. **Performance Issues**:
   - Adjust the Max Workers parameter based on your system capabilities
   - Monitor system resources during execution

### Testing Components

You can test your components independently using the provided test scripts:

```bash
cd tests
python test_all_components.py
python test_parallel_processor.py
python test_parallel_query_processor.py
python test_parallel_agent_processor.py
python verify_installation.py
```

## Development Workflow

1. Make changes to your components
2. Run the test scripts to verify functionality
3. Restart Langflow to load updated components
4. Test in the Langflow interface

## Additional Resources

- [Langflow Documentation](https://docs.langflow.org/)
- [Langflow GitHub Repository](https://github.com/logspace-ai/langflow)
