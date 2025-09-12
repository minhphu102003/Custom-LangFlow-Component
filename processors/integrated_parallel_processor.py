"""
Integrated Parallel DataFrame Processor Custom Component for Langflow.

This component processes a DataFrame with a "text" column, where each record is processed 
by an agent in parallel. Each agent can call various tools (web search, RAG, etc.) to 
answer queries based on the text value in each record.
"""

from typing import List, Dict, Any, Callable
from langflow.field_typing import Data
from langflow.template import Output
from langflow.inputs.inputs import StrInput
from threading import Lock
import json

# Import the base class
from processors.base_processor import BaseProcessor

# Import result processing functions
from utils.result_processing import combine_results_as_string, create_detailed_results_data, create_error_result_data


class IntegratedParallelProcessor(BaseProcessor):
    display_name = "Integrated Parallel Processor"
    description = "Processes DataFrame rows in parallel with integrated tool calling capabilities"
    icon = "cpu"
    name = "IntegratedParallelProcessor"
    
    # Define inputs
    inputs = [
        StrInput(
            name="dataframe_input",
            display_name="DataFrame Input",
            info="Input DataFrame with a 'text' column to process"
        ),
        StrInput(
            name="agent_system_prompt",
            display_name="Agent System Prompt",
            info="System prompt for the agent that processes each query",
            advanced=True
        ),
        StrInput(
            name="tool_configurations",
            display_name="Tool Configurations (JSON)",
            info="JSON configuration for available tools (web_search, rag_retrieve, etc.)",
            advanced=True
        ),
        StrInput(
            name="max_workers",
            display_name="Max Workers",
            info="Maximum number of parallel workers (default: 4)",
            advanced=True,
            value="4"
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
    
    def __init__(self):
        super().__init__()
        # Thread-safe lock for shared resources
        self.lock = Lock()
        self.tool_registry = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools that can be used by agents."""
        self.tool_registry["web_search"] = self._web_search_tool
        self.tool_registry["rag_retrieve"] = self._rag_retrieve_tool
        self.tool_registry["code_interpreter"] = self._code_interpreter_tool
    
    def _web_search_tool(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Simulated web search tool.
        
        Args:
            query (str): Search query
            **kwargs: Additional parameters
            
        Returns:
            Dict[str, Any]: Search results
        """
        # In a real implementation, this would call an actual web search API
        return {
            "results": [
                {"title": f"Result 1 for {query}", "snippet": f"Information about {query}..."},
                {"title": f"Result 2 for {query}", "snippet": f"More information about {query}..."}
            ],
            "total_results": 2
        }
    
    def _rag_retrieve_tool(self, query: str, dataset_id: str = "ds_demo", **kwargs) -> Dict[str, Any]:
        """
        Simulated RAG retrieval tool.
        
        Args:
            query (str): Retrieval query
            dataset_id (str): Dataset identifier
            **kwargs: Additional parameters (top_k, expand_k, etc.)
            
        Returns:
            Dict[str, Any]: Retrieved context
        """
        # In a real implementation, this would call an actual RAG retrieval system
        # Following the MCP tool usage instructions from our memory
        return {
            "documents": [
                {"content": f"Retrieved context about {query} from dataset {dataset_id}", "score": 0.95},
                {"content": f"Additional context about {query}", "score": 0.87}
            ],
            "total_documents": 2
        }
    
    def _code_interpreter_tool(self, code: str, **kwargs) -> Dict[str, Any]:
        """
        Simulated code interpreter tool.
        
        Args:
            code (str): Code to execute
            **kwargs: Additional parameters
            
        Returns:
            Dict[str, Any]: Execution results
        """
        # In a real implementation, this would execute code in a secure environment
        return {
            "output": f"Executed: {code}",
            "result": "Simulation result",
            "success": True
        }
    
    def _call_tool(self, tool_name: str, **tool_args) -> Dict[str, Any]:
        """
        Call a registered tool by name.
        
        Args:
            tool_name (str): Name of the tool to call
            **tool_args: Arguments to pass to the tool
            
        Returns:
            Dict[str, Any]: Tool response
        """
        if tool_name in self.tool_registry:
            try:
                return self.tool_registry[tool_name](**tool_args)
            except Exception as e:
                return {"error": f"Tool execution failed: {str(e)}"}
        else:
            return {"error": f"Tool '{tool_name}' not found"}
    
    def _process_single_query_with_tools(self, query_text: str) -> Dict[str, Any]:
        """
        Process a single query using an agent with tool calling capabilities.
        
        Args:
            query_text (str): The text value from the DataFrame row to process
            
        Returns:
            Dict[str, Any]: Result from processing this query
        """
        import time
        import random
        
        # Simulate agent thinking and tool calling
        processing_time = random.uniform(0.2, 1.5)
        time.sleep(processing_time)  # Simulate processing time
        
        # Simulate agent workflow:
        # 1. Analyze the query
        # 2. Decide which tools to call
        # 3. Call tools and gather information
        # 4. Synthesize final response
        
        tools_called = []
        tool_responses = []
        
        # Simulate calling different tools based on query content
        if "search" in query_text.lower() or "find" in query_text.lower():
            tools_called.append("web_search")
            response = self._call_tool("web_search", query=query_text)
            tool_responses.append(response)
        
        if "context" in query_text.lower() or "information" in query_text.lower():
            tools_called.append("rag_retrieve")
            response = self._call_tool("rag_retrieve", query=query_text, dataset_id="ds_demo")
            tool_responses.append(response)
        
        # If no specific tools were called, call web search by default
        if not tools_called:
            tools_called.append("web_search")
            response = self._call_tool("web_search", query=query_text)
            tool_responses.append(response)
        
        # Synthesize final response based on tool outputs
        if tool_responses:
            # In a real implementation, this would use an LLM to synthesize the response
            synthesized_response = f"Based on tool outputs for '{query_text}': "
            for i, (tool_name, response) in enumerate(zip(tools_called, tool_responses)):
                if "error" in response:
                    synthesized_response += f"[Error with {tool_name}: {response['error']}] "
                else:
                    synthesized_response += f"[Response from {tool_name}: {str(response)[:100]}...] "
        else:
            synthesized_response = f"Processed '{query_text}' with no tool calls."
        
        result = {
            "query": query_text,
            "response": synthesized_response.strip(),
            "tools_called": tools_called,
            "tool_responses": tool_responses,
            "processing_time": round(processing_time, 3)
        }
        
        return result
    
    def build_processed_results(self) -> str:
        """
        Build the processed results output as a combined string.
        """
        # Get the input DataFrame
        dataframe_input = self.dataframe_input
        
        try:
            # Extract text values using the base class method
            text_values = self._extract_text_values(dataframe_input)
            
            # Get max workers using the base class method
            max_workers = self._parse_max_workers(self.max_workers)
            
            # Process queries in parallel using the base class method
            results = self._process_rows_parallel(text_values, self._process_single_query_with_tools, max_workers)
            
            # Combine all results into a single string using the result processing module
            return combine_results_as_string(results, separator="\n---\n")
            
        except Exception as e:
            return f"Error processing DataFrame: {str(e)}"
    
    def build_detailed_results(self) -> Data:
        """
        Build detailed results output as structured data.
        """
        # Get the input DataFrame
        dataframe_input = self.dataframe_input
        
        try:
            # Extract text values using the base class method
            text_values = self._extract_text_values(dataframe_input)
            
            # Get max workers using the base class method
            max_workers = self._parse_max_workers(self.max_workers)
            
            # Process queries in parallel using the base class method
            results = self._process_rows_parallel(text_values, self._process_single_query_with_tools, max_workers)
            
            # Return as Langflow Data object using the result processing module
            return create_detailed_results_data(results, processor_type="integrated")
            
        except Exception as e:
            # Return error information using the result processing module
            return create_error_result_data(str(e))