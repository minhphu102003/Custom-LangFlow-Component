"""
Mock tests for ParallelAgentProcessor focusing on text extraction and worker creation.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    from processors.parallel_agent_processor import ParallelAgentProcessor
except ImportError:
    try:
        from custom_components.processors.parallel_agent_processor import ParallelAgentProcessor
    except ImportError:
        from custom_components.processors.parallel_agent_processor import ParallelAgentProcessor

from langflow.schema.data import Data


class TestParallelAgentProcessorMock(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.processor = ParallelAgentProcessor()
        
    def test_extract_text_values_with_dict_data(self):
        """Test text extraction from dictionary with 'data' key."""
        test_input = {
            "data": [
                {"text": "query1"},
                {"text": "query2"},
                {"text": "query3"}
            ]
        }
        
        # Access the base class method directly
        text_values = self.processor._extract_text_values(test_input)
        
        self.assertEqual(len(text_values), 3)
        self.assertEqual(text_values, ["query1", "query2", "query3"])
    
    def test_extract_text_values_with_text_list(self):
        """Test text extraction from dictionary with 'text' key containing list."""
        test_input = {
            "text": ["query1", "query2", "query3"]
        }
        
        # Access the base class method directly
        text_values = self.processor._extract_text_values(test_input)
        
        self.assertEqual(len(text_values), 3)
        self.assertEqual(text_values, ["query1", "query2", "query3"])
    
    def test_extract_text_values_with_list_input(self):
        """Test text extraction from list input."""
        test_input = ["query1", "query2", "query3"]
        
        # Access the base class method directly
        text_values = self.processor._extract_text_values(test_input)
        
        self.assertEqual(len(text_values), 3)
        self.assertEqual(text_values, ["query1", "query2", "query3"])
    
    def test_extract_text_values_with_single_string(self):
        """Test text extraction from single string input."""
        test_input = "single query"
        
        # Access the base class method directly
        text_values = self.processor._extract_text_values(test_input)
        
        self.assertEqual(len(text_values), 1)
        self.assertEqual(text_values, ["single query"])
    
    def test_determine_optimal_workers_small_dataframe(self):
        """Test worker determination for small DataFrames."""
        # Test with 1-4 records
        self.assertEqual(self.processor._determine_optimal_workers(1), 1)
        self.assertEqual(self.processor._determine_optimal_workers(3), 3)
        self.assertEqual(self.processor._determine_optimal_workers(4), 4)
    
    def test_determine_optimal_workers_medium_dataframe(self):
        """Test worker determination for medium DataFrames."""
        # Test with 5-8 records
        self.assertEqual(self.processor._determine_optimal_workers(5), 4)
        self.assertEqual(self.processor._determine_optimal_workers(8), 4)
    
    def test_determine_optimal_workers_large_dataframe(self):
        """Test worker determination for large DataFrames."""
        # Test with 9+ records
        self.assertEqual(self.processor._determine_optimal_workers(9), 10)
        self.assertEqual(self.processor._determine_optimal_workers(20), 10)
        self.assertEqual(self.processor._determine_optimal_workers(100), 10)
    
    @patch('helpers.agent_component.AgentComponent')
    @patch('asyncio.get_event_loop')
    def test_process_single_query_with_agent_success(self, mock_get_event_loop, mock_agent_component):
        """Test processing a single query with successful agent response."""
        # Mock the agent component
        mock_agent_instance = MagicMock()
        mock_agent_component.return_value = mock_agent_instance
        
        # Mock the asyncio event loop
        mock_loop = MagicMock()
        mock_get_event_loop.return_value = mock_loop
        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_loop.run_until_complete.return_value = mock_response
        
        # Set up processor attributes
        self.processor.system_prompt = "Test prompt"
        self.processor.agent_llm = "Google Generative AI"
        self.processor.model_name = "gemini-2.0-flash-001"
        
        # Test the method
        result = self.processor._process_single_query_with_agent("Test query")
        
        # Verify results
        self.assertTrue(result["success"])
        self.assertEqual(result["query"], "Test query")
        self.assertEqual(result["response"], "Test response")
        self.assertIsNone(result["error"])
        
        # Verify agent was created and configured correctly
        mock_agent_component.assert_called_once()
        self.assertEqual(mock_agent_instance.system_prompt, "Test prompt")
        self.assertEqual(mock_agent_instance.agent_llm, "Google Generative AI")
        self.assertEqual(mock_agent_instance.model_name, "gemini-2.0-flash-001")
        self.assertTrue(mock_agent_instance.add_current_date_tool)
    
    @patch('helpers.agent_component.AgentComponent')
    @patch('asyncio.get_event_loop')
    def test_process_single_query_with_agent_failure(self, mock_get_event_loop, mock_agent_component):
        """Test processing a single query with agent failure."""
        # Mock the agent component
        mock_agent_instance = MagicMock()
        mock_agent_component.return_value = mock_agent_instance
        
        # Mock the asyncio event loop to raise an exception
        mock_loop = MagicMock()
        mock_get_event_loop.return_value = mock_loop
        mock_loop.run_until_complete.side_effect = Exception("Test error")
        
        # Set up processor attributes
        self.processor.system_prompt = "Test prompt"
        
        # Test the method
        result = self.processor._process_single_query_with_agent("Test query")
        
        # Verify results
        self.assertFalse(result["success"])
        self.assertEqual(result["query"], "Test query")
        self.assertIsNone(result["response"])
        self.assertIn("Test error", result["error"])
    
    @patch('processors.base_processor.concurrent.futures.ThreadPoolExecutor')
    def test_process_rows_parallel(self, mock_executor_class):
        """Test parallel processing of rows."""
        # Mock the executor and its methods
        mock_executor = MagicMock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor
        
        # Mock the future results
        mock_future1 = MagicMock()
        mock_future2 = MagicMock()
        mock_future1.result.return_value = {"query": "query1", "response": "response1", "success": True}
        mock_future2.result.return_value = {"query": "query2", "response": "response2", "success": True}
        
        mock_executor.submit.side_effect = [mock_future1, mock_future2]
        mock_completed = [mock_future1, mock_future2]
        
        # Mock as_completed function
        with patch('processors.base_processor.concurrent.futures.as_completed', return_value=mock_completed):
            # Define a simple processing function
            def process_func(text):
                return {"query": text, "response": f"response for {text}", "success": True}
            
            # Test the method
            text_values = ["query1", "query2"]
            results = self.processor._process_rows_parallel(text_values, process_func, max_workers=2)
            
            # Verify results
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0]["query"], "query1")
            self.assertEqual(results[1]["query"], "query2")
            
            # Verify ThreadPoolExecutor was called with correct parameters
            mock_executor_class.assert_called_with(max_workers=2)


if __name__ == '__main__':
    unittest.main()