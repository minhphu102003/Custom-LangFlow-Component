"""
Base Processor Class for Langflow Custom Components.

This module provides a base class that contains common functionality 
shared across all processor components to reduce code duplication.

The BaseProcessor class provides:
- Thread-safe operations with locking mechanisms
- Standardized data extraction from various DataFrame formats
- Parallel processing capabilities using ThreadPoolExecutor
- Error handling and result standardization
- Utility methods for common operations

All processor components should inherit from this class to leverage
the shared functionality and maintain consistency across the codebase.
"""

from typing import List, Dict, Any, Callable
from langflow.custom import Component
from langflow.field_typing import Data
from threading import Lock
import concurrent.futures
from utils.utils import extract_text_values, parse_max_workers


class BaseProcessor(Component):
    """
    Base class for all processor components.
    
    This class provides common functionality that is shared across all
    processor components in the custom components package. It handles
    data extraction, parallel processing, error handling, and other
    common operations.
    
    Attributes:
        lock (Lock): Thread-safe lock for shared resources
        results_cache (dict): Cache for storing processed results
    """
    
    def __init__(self):
        """
        Initialize the BaseProcessor.
        
        Sets up the thread-safe lock and results cache.
        """
        super().__init__()
        # Thread-safe lock for shared resources
        self.lock = Lock()
        self.results_cache = {}
    
    def _extract_text_values(self, dataframe_input: Any) -> List[str]:
        """
        Extract text values from the input DataFrame.
        
        This method handles various input formats and extracts the text
        values from the 'text' column of the DataFrame.
        
        Args:
            dataframe_input: Input DataFrame with 'text' column.
                Can be a Langflow Data object, dictionary, list, or single value.
            
        Returns:
            List[str]: List of text values extracted from the DataFrame.
            
        Example:
            >>> processor = BaseProcessor()
            >>> data = {"data": [{"text": "query1"}, {"text": "query2"}]}
            >>> processor._extract_text_values(data)
            ['query1', 'query2']
        """
        return extract_text_values(dataframe_input)
    
    def _process_rows_parallel(self, text_values: List[str], process_func: Callable, max_workers: int = 4) -> List[Dict[str, Any]]:
        """
        Process multiple rows in parallel using ThreadPoolExecutor.
        
        This method takes a list of text values and processes each one
        using the provided processing function in parallel.
        
        Args:
            text_values (List[str]): List of text values to process.
            process_func (Callable): Function to process each text value.
                Must accept a single string argument and return a dict.
            max_workers (int): Maximum number of parallel workers.
                Defaults to 4.
            
        Returns:
            List[Dict[str, Any]]: List of results from processing each row.
                Each result is a dictionary containing the processing outcome.
        """
        results = []
        
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_text = {
                executor.submit(process_func, text_value): text_value 
                for text_value in text_values
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_text):
                text_value = future_to_text[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    # Handle exceptions in individual tasks
                    error_result = self._create_error_result(text_value, str(e))
                    results.append(error_result)
        
        return results
    
    def _create_error_result(self, query_text: str, error_message: str) -> Dict[str, Any]:
        """
        Create a standardized error result structure.
        
        This method creates a consistent error result format that can be
        used across all processor components.
        
        Args:
            query_text (str): The text that caused the error.
            error_message (str): The error message.
            
        Returns:
            Dict[str, Any]: Standardized error result with the following keys:
                - query: The text that caused the error
                - response: Formatted error message
                - tools_called: Empty list (no tools called in error case)
                - processing_time: 0 (no processing time for errors)
                - error: True (indicates this is an error result)
        """
        return {
            "query": query_text,
            "response": f"Error processing query: {error_message}",
            "tools_called": [],
            "processing_time": 0,
            "error": True
        }
    
    def _parse_max_workers(self, max_workers_input: Any, default: int = 4) -> int:
        """
        Parse max_workers input to an integer.
        
        This method safely converts the max_workers input to an integer,
        handling various input types and providing a default value if
        parsing fails.
        
        Args:
            max_workers_input: Input value for max workers.
                Can be a string, integer, or other type.
            default (int): Default value if parsing fails.
                Defaults to 4.
            
        Returns:
            int: Parsed max workers value.
        """
        return parse_max_workers(max_workers_input, default)