"""
Parallel Query Processor Custom Component for Langflow.

This component processes a DataFrame with a "text" column in parallel, where each row 
contains a query that is processed independently by an agent. The final output is 
the aggregated results from all agents.
"""

from typing import List, Dict, Any
from langflow.inputs.inputs import StrInput
from langflow.template import Output
from langflow.field_typing import Data
import json

# Import the base class
from processors.base_processor import BaseProcessor

# Import result processing functions
from utils.result_processing import combine_results_as_string, create_detailed_results_data, create_error_result_data


class ParallelQueryProcessor(BaseProcessor):
    display_name = "Parallel Query Processor"
    description = "Processes DataFrame rows in parallel, with each row processed by an agent to answer queries"
    icon = "activity"
    name = "ParallelQueryProcessor"
    
    # Define inputs
    inputs = [
        StrInput(
            name="dataframe_input",
            display_name="DataFrame Input",
            info="Input DataFrame with a 'text' column containing queries to process"
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
            display_name="Combined Results",
            name="combined_results",
            method="build_combined_results"
        ),
        Output(
            display_name="Detailed Results",
            name="detailed_results",
            method="build_detailed_results"
        )
    ]
    
    def _process_single_query(self, query_text: str) -> Dict[str, Any]:
        """
        Process a single query with an agent.
        In a real implementation, this would call actual agent logic.
        
        Args:
            query_text (str): The query text to process
            
        Returns:
            Dict[str, Any]: Result from processing this query
        """
        # Simulate agent processing
        import time
        import random
        processing_time = random.uniform(0.1, 0.5)
        time.sleep(processing_time)  # Simulate processing time
        
        # In a real implementation, this would:
        # 1. Initialize an agent
        # 2. Call tools as needed (web search, RAG, etc.)
        # 3. Generate a response based on the tools' outputs
        
        result = {
            "query": query_text,
            "answer": f"Answer to '{query_text}'",
            "processing_time": round(processing_time, 3)
        }
        
        return result
    
    def build_combined_results(self) -> str:
        """
        Build the combined results output as a single string.
        """
        try:
            # Extract queries from the input DataFrame using the base class method
            queries = self._extract_text_values(self.dataframe_input)
            
            # Get max workers using the base class method
            max_workers = self._parse_max_workers(self.max_workers)
            
            # Process queries in parallel using the base class method
            results = self._process_rows_parallel(queries, self._process_single_query, max_workers)
            
            # Combine all results into a single string using the result processing module
            return combine_results_as_string(results)
            
        except Exception as e:
            return f"Error processing queries: {str(e)}"
    
    def build_detailed_results(self) -> Data:
        """
        Build detailed results output as structured data.
        """
        try:
            # Extract queries from the input DataFrame using the base class method
            queries = self._extract_text_values(self.dataframe_input)
            
            # Get max workers using the base class method
            max_workers = self._parse_max_workers(self.max_workers)
            
            # Process queries in parallel using the base class method
            results = self._process_rows_parallel(queries, self._process_single_query, max_workers)
            
            # Return as Langflow Data object using the result processing module
            return create_detailed_results_data(results, processor_type="query")
            
        except Exception as e:
            # Return error information using the result processing module
            return create_error_result_data(str(e))