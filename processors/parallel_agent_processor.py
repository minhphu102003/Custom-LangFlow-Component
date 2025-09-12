"""
Parallel Agent Processor Custom Component for Langflow.

This component processes a DataFrame with a "text" column, where each record is processed 
by multiple AgentComponent instances in parallel. Each agent can call tools from an MCP 
server via SSE to answer queries based on the text value in each record.

The number of workers is dynamically determined based on the number of records in the DataFrame.
"""

import sys
import os
from typing import List, Dict, Any, Callable, Optional
from langflow.custom import Component
from langflow.field_typing import Data, Tool
from langflow.template import Output
from langflow.inputs.inputs import StrInput, HandleInput
import json
import concurrent.futures

# Import the base processor
from .base_processor import BaseProcessor

# Import result processing functions
try:
    from utils.result_processing import combine_results_as_string, create_detailed_results_data, create_error_result_data
except ImportError:
    try:
        from ..utils.result_processing import combine_results_as_string, create_detailed_results_data, create_error_result_data
    except ImportError:
        # Fallback implementations if imports fail
        def combine_results_as_string(results: List[Dict[str, Any]], separator: str = "\n") -> str:
            if not results:
                return ""
            return separator.join([str(result.get("response", "")) for result in results])
        
        def create_detailed_results_data(results: List[Dict[str, Any]], processor_type: str = "generic", additional_stats: Optional[Dict[str, Any]] = None) -> Data:
            return Data(data={"results": results, "processor_type": processor_type})
        
        def create_error_result_data(error_message: str) -> Data:
            return Data(data={"error": error_message})

# Import the AgentComponent
try:
    from processors.agent_component import AgentComponent
except ImportError:
    try:
        from .agent_component import AgentComponent
    except ImportError:
        AgentComponent = None

class ParallelAgentProcessor(BaseProcessor):
    display_name = "Parallel Agent Processor"
    description = "Processes DataFrame rows in parallel using multiple AgentComponent instances that can call MCP server tools via SSE. Number of workers based on DataFrame size."
    icon = "users"
    name = "ParallelAgentProcessor"
    
    # Define inputs
    inputs = [
        StrInput(
            name="dataframe_input",
            display_name="DataFrame Input",
            info="Input DataFrame with a 'text' column to process"
        ),
        StrInput(
            name="system_prompt",
            display_name="Agent System Prompt",
            info="System prompt for the agents that process queries",
            advanced=True,
            value="You are a helpful assistant that can use tools to answer questions and perform tasks."
        ),
        StrInput(
            name="agent_llm",
            display_name="Agent LLM Provider",
            info="Language model provider for the agents",
            advanced=True,
            value="Google Generative AI"
        ),
        StrInput(
            name="model_name",
            display_name="Model Name",
            info="Specific model name to use for the agents",
            advanced=True,
            value="gemini-2.0-flash-001"
        ),
        HandleInput(
            name="mcp_server",
            display_name="MCP Server",
            info="MCP server to connect to for tools",
            advanced=True,
            input_types=["MCPTools"]
        )
    ]
    
    # Define outputs
    outputs = [
        Output(
            display_name="Processed Results",
            name="processed_results",
            method="build_processed_results"
        ),
        Output(
            display_name="Detailed Results",
            name="detailed_results",
            method="build_detailed_results"
        )
    ]
    
    def _determine_optimal_workers(self, record_count: int) -> int:
        """
        Determine the optimal number of workers based on the number of records.
        
        Args:
            record_count (int): Number of records in the DataFrame
            
        Returns:
            int: Optimal number of workers (between 1 and 10)
        """
        # For small DataFrames, use one worker per record
        if record_count <= 4:
            return max(1, record_count)
        # For medium DataFrames, use a balanced approach
        elif record_count <= 8:
            return 4
        # For larger DataFrames, cap at 10 workers to avoid overwhelming the system
        else:
            return 10
    
    def _process_single_query_with_agent(self, query_text: str) -> Dict[str, Any]:
        """
        Process a single query using one AgentComponent instance.
        
        Args:
            query_text (str): The text value from the DataFrame row to process
            
        Returns:
            Dict[str, Any]: Result from processing this query
        """
        try:
            # Get system prompt
            system_prompt = getattr(self, "system_prompt", "You are a helpful assistant that can use tools to answer questions and perform tasks.")
            
            # Get MCP server if available
            mcp_server = getattr(self, "mcp_server", None)
            
            # Get model configuration if available
            agent_llm = getattr(self, "agent_llm", "Google Generative AI")
            model_name = getattr(self, "model_name", "gemini-2.0-flash-001")
            
            # Check if AgentComponent is available
            if AgentComponent is None:
                raise ImportError("AgentComponent could not be imported")
            
            # Create agent component instance
            agent = AgentComponent()
            
            # Set parameters for the agent
            agent.system_prompt = system_prompt
            # Create a proper Message object for input_value
            from langflow.schema.message import Message
            agent.input_value = Message(text=query_text)
            agent.add_current_date_tool = True
            
            # Set model configuration
            agent.agent_llm = agent_llm
            agent.model_name = model_name
            
            # Set Google API key from environment variable
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if google_api_key:
                agent.api_key = google_api_key
            
            # Add MCP server tool if available
            if mcp_server:
                # Initialize tools list if it doesn't exist
                if not hasattr(agent, 'tools') or agent.tools is None:
                    agent.tools = []
                # Add the MCP server tool to the agent's tools
                if isinstance(agent.tools, list):
                    agent.tools.append(mcp_server)
                else:
                    agent.tools = [mcp_server]
            
            # Process the query with this agent
            import asyncio
            try:
                # Try to get the current event loop
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # If no event loop exists, create a new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run the async method in the event loop
            response = loop.run_until_complete(agent.message_response())
            
            return {
                "query": query_text,
                "response": response.text if hasattr(response, 'text') else str(response),
                "success": True,
                "error": None
            }
            
        except Exception as e:
            return {
                "query": query_text,
                "response": None,
                "success": False,
                "error": str(e)
            }
    
    def build_processed_results(self) -> str:
        """
        Build the processed results output as a combined string.
        The number of workers is dynamically determined based on DataFrame size.
        """
        # Get the input DataFrame
        dataframe_input = self.dataframe_input
        
        try:
            # Extract text values using the base class method
            text_values = self._extract_text_values(dataframe_input)
            
            # Determine optimal number of workers based on DataFrame size
            record_count = len(text_values)
            max_workers = self._determine_optimal_workers(record_count)
            
            # Process rows in parallel using the base class method
            results = self._process_rows_parallel(text_values, self._process_single_query_with_agent, max_workers)
            
            # Combine all results into a single string using the result processing module
            return combine_results_as_string(results)
            
        except Exception as e:
            return f"Error processing DataFrame: {str(e)}"
    
    def build_detailed_results(self) -> Data:
        """
        Build detailed results output as structured data.
        The number of workers is dynamically determined based on DataFrame size.
        """
        # Get the input DataFrame
        dataframe_input = self.dataframe_input
        
        try:
            # Extract text values using the base class method
            text_values = self._extract_text_values(dataframe_input)
            
            # Determine optimal number of workers based on DataFrame size
            record_count = len(text_values)
            max_workers = self._determine_optimal_workers(record_count)
            
            # Process rows in parallel using the base class method
            results = self._process_rows_parallel(text_values, self._process_single_query_with_agent, max_workers)
            
            # Return as Langflow Data object using the result processing module
            return create_detailed_results_data(results, processor_type="parallel_agents")
            
        except Exception as e:
            # Return error information using the result processing module
            return create_error_result_data(str(e))