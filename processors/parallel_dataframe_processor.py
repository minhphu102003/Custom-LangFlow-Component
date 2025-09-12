"""
Parallel DataFrame Processor Custom Component for Langflow.

This component processes a DataFrame with a "text" column, where each record is processed 
by an agent in parallel. Each agent calls tools to answer queries based on the text value 
in each record, and the component outputs the combined results from all agents.
"""

from typing import List, Dict, Any
from langflow.field_typing import Data
from langflow.template import Output
from langflow.inputs.inputs import StrInput
import json

# Import the base class
from processors.base_processor import BaseProcessor

# Import result processing functions
from utils.result_processing import combine_results_as_string, create_detailed_results_data, create_error_result_data


class ParallelDataFrameProcessor(BaseProcessor):
    display_name = "Parallel DataFrame Processor"
    description = "Processes DataFrame rows in parallel, with each row processed by an agent that calls tools to answer queries"
    icon = "parallel"
    name = "ParallelDataFrameProcessor"
    
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
        
        # Simulate agent processing with some variation in processing time
        import time
        import random
        processing_time = random.uniform(0.1, 1.0)
        time.sleep(processing_time)  # Simulate processing time
        
        result = {
            "query": query_text,
            "response": f"Processed response for: {query_text}",
            "tools_called": ["web_search"],
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
            
            # Process rows in parallel using the base class method
            results = self._process_rows_parallel(text_values, self._process_single_row, max_workers)
            
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
            
            # Get max workers using the base class method
            max_workers = self._parse_max_workers(self.max_workers)
            
            # Process rows in parallel using the base class method
            results = self._process_rows_parallel(text_values, self._process_single_row, max_workers)
            
            # Return as Langflow Data object using the result processing module
            return create_detailed_results_data(results, processor_type="parallel")
            
        except Exception as e:
            # Return error information using the result processing module
            return create_error_result_data(str(e))