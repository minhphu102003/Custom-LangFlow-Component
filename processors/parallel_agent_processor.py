"""
Parallel Agent Processor Custom Component for Langflow.

This component processes a DataFrame with a "text" column, where each record is processed 
by multiple AgentComponent instances in parallel. Each agent can call tools from an MCP 
server via SSE to answer queries based on the text value in each record.

The number of workers is dynamically determined based on the number of records in the DataFrame.
"""

from typing import List, Dict, Any, Callable, Optional
from langflow.custom import Component
from langflow.field_typing import Data, Tool
from langflow.template import Output
from langflow.inputs.inputs import StrInput, HandleInput
import json
import concurrent.futures

# Import the base class
from .base_processor import BaseProcessor

# Import result processing functions
from ..utils.result_processing import combine_results_as_string, create_detailed_results_data, create_error_result_data

# Import the agent component wrapper
from .agent_component_wrapper import AgentComponentWrapper

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
            name="agent_count",
            display_name="Agent Count",
            info="Number of agents to use for processing each query (default: 3)",
            advanced=True,
            value="3"
        ),
        StrInput(
            name="max_workers",
            display_name="Max Workers",
            info="Maximum number of parallel workers (default: based on DataFrame size, max 10)",
            advanced=True,
            value=""
        ),
        StrInput(
            name="system_prompt",
            display_name="Agent System Prompt",
            info="System prompt for the agents that process queries",
            advanced=True,
            value="You are a helpful assistant that can use tools to answer questions and perform tasks."
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
    
    def _process_single_query_with_multiple_agents(self, query_text: str) -> Dict[str, Any]:
        """
        Process a single query using multiple AgentComponent instances with MCP server tools via SSE.
        
        Args:
            query_text (str): The text value from the DataFrame row to process
            
        Returns:
            Dict[str, Any]: Result from processing this query with multiple agents
        """
        try:
            # Get the number of agents to use
            agent_count = int(getattr(self, "agent_count", "3")) or 3
            
            # Get system prompt
            system_prompt = getattr(self, "system_prompt", "You are a helpful assistant that can use tools to answer questions and perform tasks.")
            
            # Get MCP server if available
            mcp_server = getattr(self, "mcp_server", None)
            
            # Import the agent component class
            from .agent_implementation_example import ResponseEnhancementAgent
            
            # Create multiple agents and process the query
            agent_responses = []
            tools_called = []
            agents_called = []
            
            # Process query with multiple agents
            for i in range(agent_count):
                # Create agent component wrapper with the required agent_component_class parameter
                agent_wrapper = AgentComponentWrapper(
                    agent_component_class=ResponseEnhancementAgent,
                    system_prompt=system_prompt,
                    mcp_server=mcp_server
                )
                
                # Process the query with this agent
                agent_result = agent_wrapper.process_query(query_text)
                agent_responses.append(agent_result)
                
                # Track agents and tools called
                agents_called.append(f"Agent_{i+1}")
                if 'tools_called' in agent_result:
                    tools_called.extend(agent_result['tools_called'])
            
            # Combine results from all agents
            combined_response = {
                "query": query_text,
                "response": [result.get("response", "") for result in agent_responses],
                "agents_called": agents_called,
                "tools_called": list(set(tools_called)),  # Remove duplicates
                "agent_responses": agent_responses,
                "processing_time": sum(result.get("processing_time", 0) for result in agent_responses if "processing_time" in result),
                "error": None
            }
            
            return combined_response
            
        except Exception as e:
            # Return error result if processing fails
            return {
                "query": query_text,
                "response": f"Error processing query: {str(e)}",
                "agents_called": [],
                "tools_called": [],
                "agent_responses": [],
                "processing_time": 0,
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
            if hasattr(self, "max_workers") and self.max_workers:
                # Use specified max_workers if provided
                max_workers = self._parse_max_workers(self.max_workers, default=self._determine_optimal_workers(record_count))
            else:
                # Automatically determine based on record count
                max_workers = self._determine_optimal_workers(record_count)
            
            # Process rows in parallel using the base class method
            results = self._process_rows_parallel(text_values, self._process_single_query_with_multiple_agents, max_workers)
            
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
            if hasattr(self, "max_workers") and self.max_workers:
                # Use specified max_workers if provided
                max_workers = self._parse_max_workers(self.max_workers, default=self._determine_optimal_workers(record_count))
            else:
                # Automatically determine based on record count
                max_workers = self._determine_optimal_workers(record_count)
            
            # Process rows in parallel using the base class method
            results = self._process_rows_parallel(text_values, self._process_single_query_with_multiple_agents, max_workers)
            
            # Return as Langflow Data object using the result processing module
            return create_detailed_results_data(results, processor_type="parallel_agents")
            
        except Exception as e:
            # Return error information using the result processing module
            return create_error_result_data(str(e))