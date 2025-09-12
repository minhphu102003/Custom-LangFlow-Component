"""
Result Processing Module for Langflow Custom Components.

This module contains functions for processing and formatting results 
from the various processor components. It provides standardized ways
to combine results into strings and create detailed data objects.

Functions:
    combine_results_as_string: Combine results into a formatted string
    create_detailed_results_data: Create detailed results as Langflow Data object
    create_error_result_data: Create error result as Langflow Data object
"""

from typing import List, Dict, Any, Optional
from langflow.field_typing import Data
import json


def combine_results_as_string(results: List[Dict[str, Any]], separator: str = "\n") -> str:
    """
    Combine results into a single string.
    
    This function takes a list of result dictionaries and combines them
    into a single formatted string. The format depends on the structure
    of the result dictionaries.
    
    Args:
        results (List[Dict[str, Any]]): List of result dictionaries.
            Each dictionary should represent the result of processing
            a single input item.
        separator (str): Separator to use between results.
            Defaults to newline character.
        
    Returns:
        str: Combined results as a single formatted string.
        
    Result formats supported:
        1. Dataframe processor results with 'response' key
        2. Query processor results with 'query' and 'answer' keys
        3. Generic results converted to JSON
        
    Example:
        >>> results = [{"response": "Answer 1"}, {"response": "Answer 2"}]
        >>> combine_results_as_string(results)
        'Answer 1\\nAnswer 2'
        
        >>> results = [{"query": "Q1", "answer": "A1"}, {"query": "Q2", "answer": "A2"}]
        >>> combine_results_as_string(results)
        'Q: Q1\\nA: A1\\nQ: Q2\\nA: A2'
    """
    if not results:
        return ""
    
    # Check if results have 'response' key (dataframe processors)
    if "response" in results[0]:
        return separator.join([result["response"] for result in results])
    
    # Check if results have 'answer' key (query processor)
    if "answer" in results[0]:
        return separator.join([
            f"Q: {result['query']}\nA: {result['answer']}" 
            for result in results
        ])
    
    # Fallback: convert to JSON
    return separator.join([json.dumps(result, separators=(',', ':')) for result in results])


def create_detailed_results_data(
    results: List[Dict[str, Any]], 
    processor_type: str = "generic",
    additional_stats: Optional[Dict[str, Any]] = None
) -> Data:
    """
    Create detailed results as Langflow Data object.
    
    This function takes a list of result dictionaries and creates a
    comprehensive Langflow Data object with detailed statistics and
    metadata.
    
    Args:
        results (List[Dict[str, Any]]): List of result dictionaries.
        processor_type (str): Type of processor for statistics.
            Supported values: "simple", "parallel", "integrated", "query", "generic".
            Defaults to "generic".
        additional_stats (Dict[str, Any]): Additional statistics to include.
            Optional dictionary with custom statistics.
        
    Returns:
        Data: Langflow Data object with detailed results and statistics.
        
    Statistics included:
        - Total processed items
        - Successful processing count
        - Failed processing count
        - Total processing time
        - Average processing time
        - Processor type
        - Timestamp
        - Tool usage (for integrated and parallel processors)
        - Total queries (for query processor)
        
    Example:
        >>> results = [{"response": "Answer 1", "processing_time": 0.5}, 
        ...            {"response": "Answer 2", "processing_time": 0.3}]
        >>> data = create_detailed_results_data(results, "parallel")
        >>> data.data["total_processed"]
        2
    """
    # Calculate basic statistics
    total_processed = len(results)
    successful = len([r for r in results if not r.get("error")])
    failed = total_processed - successful
    total_time = sum([r.get("processing_time", 0) for r in results])
    
    # Create base data structure
    data = {
        "results": results,
        "total_processed": total_processed,
        "successful": successful,
        "failed": failed,
        "total_processing_time": round(total_time, 3),
        "average_processing_time": round(total_time / total_processed if total_processed > 0 else 0, 3),
        "processor_type": processor_type,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }
    
    # Add additional statistics if provided
    if additional_stats:
        data.update(additional_stats)
    
    # Add processor-specific fields
    if processor_type == "query":
        data["total_queries"] = total_processed
    
    # Add tool usage statistics if available
    if processor_type in ["integrated", "parallel"]:
        tool_usage = {}
        for result in results:
            for tool in result.get("tools_called", []):
                tool_usage[tool] = tool_usage.get(tool, 0) + 1
        data["tool_usage"] = tool_usage
    
    return Data(data=data)


def create_error_result_data(error_message: str) -> Data:
    """
    Create error result as Langflow Data object.
    
    This function creates a standardized error result as a Langflow
    Data object with error information and timestamp.
    
    Args:
        error_message (str): Error message to include in the result.
        
    Returns:
        Data: Langflow Data object with error information.
        
    Example:
        >>> error_data = create_error_result_data("Connection failed")
        >>> "error" in error_data.data
        True
    """
    return Data(
        data={
            "error": error_message,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
    )