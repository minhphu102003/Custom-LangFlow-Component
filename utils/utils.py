"""
Utility functions for the custom components.

This module contains shared utility functions that can be used across 
different components to reduce code duplication and improve maintainability.

Functions:
    extract_text_values: Extract text values from various DataFrame formats
    parse_max_workers: Safely parse max_workers input to an integer
"""

from typing import List, Any


def extract_text_values(dataframe_input: Any) -> List[str]:
    """
    Extract text values from the input DataFrame.
    
    This function handles various input formats and extracts the text
    values from the 'text' column of the DataFrame.
    
    Args:
        dataframe_input: Input DataFrame with 'text' column.
            Can be a Langflow Data object, dictionary, list, or single value.
        
    Returns:
        List[str]: List of text values extracted from the DataFrame.
        
    Supported input formats:
        1. Langflow Data object with 'data' attribute containing a list of dicts
        2. Dictionary with 'data' key containing a list of dicts
        3. Dictionary with 'text' key containing a list of strings
        4. List or tuple of strings
        5. Single string value
        
    Example:
        >>> data = {"data": [{"text": "query1"}, {"text": "query2"}]}
        >>> extract_text_values(data)
        ['query1', 'query2']
        
        >>> data = {"text": ["query1", "query2"]}
        >>> extract_text_values(data)
        ['query1', 'query2']
        
        >>> data = ["query1", "query2"]
        >>> extract_text_values(data)
        ['query1', 'query2']
    """
    text_values = []
    
    # Handle different possible input formats
    if hasattr(dataframe_input, 'data') and isinstance(dataframe_input.data, list):
        # Langflow Data object
        for item in dataframe_input.data:
            if isinstance(item, dict) and 'text' in item:
                text_values.append(item['text'])
    elif isinstance(dataframe_input, dict):
        # Dictionary representation
        if 'data' in dataframe_input and isinstance(dataframe_input['data'], list):
            for item in dataframe_input['data']:
                if isinstance(item, dict) and 'text' in item:
                    text_values.append(item['text'])
        elif 'text' in dataframe_input and isinstance(dataframe_input['text'], list):
            # Direct 'text' column
            text_values = dataframe_input['text']
    elif isinstance(dataframe_input, (list, tuple)):
        # List or tuple of values
        text_values = list(dataframe_input)
    else:
        # Single value
        text_values = [str(dataframe_input)]
        
    return text_values


def parse_max_workers(max_workers_input: Any, default: int = 4) -> int:
    """
    Parse max_workers input to an integer.
    
    This function safely converts the max_workers input to an integer,
    handling various input types and providing a default value if
    parsing fails.
    
    Args:
        max_workers_input: Input value for max workers.
            Can be a string, integer, or other type.
        default (int): Default value if parsing fails.
            Defaults to 4.
        
    Returns:
        int: Parsed max workers value.
        
    Example:
        >>> parse_max_workers("4", 2)
        4
        >>> parse_max_workers(8, 2)
        8
        >>> parse_max_workers(None, 2)
        2
        >>> parse_max_workers("invalid", 2)
        2
    """
    try:
        return int(max_workers_input) if max_workers_input else default
    except (ValueError, TypeError):
        return default