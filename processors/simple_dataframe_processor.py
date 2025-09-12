"""
Simple DataFrame Processor Custom Component for Langflow.

This component processes a DataFrame with a "text" column, where each record is processed 
by an agent. Each agent calls tools to answer queries based on the text value 
in each record, and the component outputs the combined results from all agents.
"""

from typing import List, Dict, Any
from langflow.custom import Component
from langflow.field_typing import Data
from langflow.inputs.inputs import StrInput
from langflow.template import Output
import json

# Import the base class
from processors.base_processor import BaseProcessor

# Import result processing functions
from utils.result_processing import combine_results_as_string, create_detailed_results_data, create_error_result_data


class SimpleDataFrameProcessor(BaseProcessor):
    display_name = "Simple DataFrame Processor"
    description = "Processes DataFrame rows with agents that call tools to answer queries"
    icon = "table"
    name = "SimpleDataFrameProcessor"
    
    # Define inputs
    inputs = [
        StrInput(
            name="dataframe_input",
            display_name="DataFrame Input",
            info="Input DataFrame with a 'text' column to process"
        ),
        StrInput(
            name="agent_prompt_template",
            display_name="Agent Prompt Template",
            info="Template for the agent prompt, with {query} placeholder for each text value",
            advanced=True
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
    
    def _process_single_row(self, query_text: str) -> Dict[str, Any]:
        """
        Process a single row with an agent.
        In a real implementation, this would call actual agent logic and tools.
        
        Args:
            query_text (str): The text value from the DataFrame row to process
            
        Returns:
            Dict[str, Any]: Result from processing this query
        """
        # This is a placeholder implementation
        # In a real scenario, this would:
        # 1. Initialize an agent with the provided prompt template
        # 2. Call tools as needed (web search, RAG, etc.)
        # 3. Generate a response based on the tools' outputs
        
        # Simulate agent processing
        result = {
            "query": query_text,
            "response": f"Processed response for: {query_text}",
            "tools_called": ["web_search"],
            "processing_time": 0.5  # Simulated time
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
            
            # Process each text value
            results = []
            for text_value in text_values:
                result = self._process_single_row(text_value)
                results.append(result)
            
            # Combine all results into a single string using the result processing module
            return combine_results_as_string(results)
            
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
            
            # Process each text value
            results = []
            for text_value in text_values:
                result = self._process_single_row(text_value)
                results.append(result)
            
            # Return as Langflow Data object using the result processing module
            return create_detailed_results_data(results, processor_type="simple")
            
        except Exception as e:
            # Return error information using the result processing module
            return create_error_result_data(str(e))