"""
Unit tests for the _extract_text_from_inputs method in ParallelTextAgentProcessor.
"""

import sys
import os
import unittest
from unittest.mock import Mock

# Add the parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from processors.parallel_text_agent import ParallelTextAgentProcessor


class TestDataFrameExtraction(unittest.TestCase):
    """Test cases for DataFrame input handling in _extract_text_from_inputs method."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.processor = ParallelTextAgentProcessor()
    
    def test_extract_text_from_dataframe_with_dict_data(self):
        """Test extracting text from DataFrame-like dict with 'data' key."""
        # Create a DataFrame-like input with 'data' key containing text records
        dataframe_input = {
            "data": [
                {"text": "What is artificial intelligence?"},
                {"text": "How does machine learning work?"},
                {"text": "Explain neural networks"}
            ]
        }
        
        # Extract text values
        result = self.processor._extract_text_from_inputs(dataframe_input)
        
        # Verify the result
        expected = [
            "What is artificial intelligence?",
            "How does machine learning work?",
            "Explain neural networks"
        ]
        self.assertEqual(result, expected)
    
    def test_extract_text_from_dataframe_with_langflow_data_object(self):
        """Test extracting text from Langflow Data object."""
        # Create a mock Langflow Data object
        mock_data_object = Mock()
        mock_data_object.data = [
            {"text": "What is deep learning?"},
            {"text": "Explain reinforcement learning"},
            {"text": "What is natural language processing?"}
        ]
        
        # Extract text values
        result = self.processor._extract_text_from_inputs(mock_data_object)
        
        # Verify the result
        expected = [
            "What is deep learning?",
            "Explain reinforcement learning",
            "What is natural language processing?"
        ]
        self.assertEqual(result, expected)
    
    def test_extract_text_from_list_of_strings(self):
        """Test extracting text from list of strings."""
        # Create a list of strings input
        list_input = [
            "What is artificial intelligence?",
            "How does machine learning work?",
            "Explain neural networks"
        ]
        
        # Extract text values
        result = self.processor._extract_text_from_inputs(list_input)
        
        # Verify the result
        expected = [
            "What is artificial intelligence?",
            "How does machine learning work?",
            "Explain neural networks"
        ]
        self.assertEqual(result, expected)
    
    def test_extract_text_from_single_string(self):
        """Test extracting text from single string."""
        # Create a single string input
        single_input = "What is artificial intelligence?"
        
        # Extract text values
        result = self.processor._extract_text_from_inputs(single_input)
        
        # Verify the result
        expected = ["What is artificial intelligence?"]
        self.assertEqual(result, expected)
    
    def test_extract_text_from_empty_dataframe(self):
        """Test extracting text from empty DataFrame."""
        # Create an empty DataFrame-like input
        dataframe_input = {"data": []}
        
        # Extract text values
        result = self.processor._extract_text_from_inputs(dataframe_input)
        
        # Verify the result is an empty list
        self.assertEqual(result, [])
    
    def test_extract_text_from_dataframe_with_mixed_content(self):
        """Test extracting text from DataFrame with mixed content types."""
        # Create a DataFrame-like input with mixed content
        dataframe_input = {
            "data": [
                {"text": "What is artificial intelligence?"},
                "Simple string entry",
                {"text": "Explain neural networks"}
            ]
        }
        
        # Extract text values
        result = self.processor._extract_text_from_inputs(dataframe_input)
        
        # Verify the result - strings should be converted to their string representation
        expected = [
            "What is artificial intelligence?",
            "Simple string entry",
            "Explain neural networks"
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    print("Testing _extract_text_from_inputs method")
    print("=" * 50)
    
    # Run the tests
    unittest.main(verbosity=2)