"""
Unit tests for parallel processing functionality in ParallelTextAgentProcessor.
"""

import sys
import os
import time
import unittest
from unittest.mock import Mock, patch
from concurrent.futures import ThreadPoolExecutor

# Add the parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from processors.parallel_text_agent import ParallelTextAgentProcessor



class TestParallelProcessing(unittest.TestCase):
    """Test cases for parallel processing functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.processor = ParallelTextAgentProcessor()
    
    def test_determine_optimal_workers_small_dataframe(self):
        """Test optimal worker determination for small DataFrames."""
        # Test with 1-4 records (should return record count)
        for record_count in [1, 2, 3, 4]:
            workers = self.processor._determine_optimal_workers(record_count)
            self.assertEqual(workers, record_count)
    
    def test_determine_optimal_workers_medium_dataframe(self):
        """Test optimal worker determination for medium DataFrames."""
        # Test with 5-8 records (should return 4 workers)
        for record_count in [5, 6, 7, 8]:
            workers = self.processor._determine_optimal_workers(record_count)
            self.assertEqual(workers, 4)
    
    def test_determine_optimal_workers_large_dataframe(self):
        """Test optimal worker determination for large DataFrames."""
        # Test with 9+ records (should return 10 workers)
        for record_count in [9, 10, 20, 50, 100]:
            workers = self.processor._determine_optimal_workers(record_count)
            self.assertEqual(workers, 10)
    
    def test_process_rows_parallel_with_multiple_workers(self):
        """Test parallel processing with multiple workers."""
        # Create test data
        text_values = [
            "Query 1",
            "Query 2", 
            "Query 3",
            "Query 4",
            "Query 5"
        ]
        
        # Define a simple processing function that simulates work
        def process_func(text_item):
            # Simulate some processing time
            time.sleep(0.1)
            return {
                "input_text": text_item,
                "response": f"Response to {text_item}",
                "success": True
            }
        
        # Measure time for parallel processing
        start_time = time.time()
        results = self.processor._process_rows_parallel(text_values, process_func, max_workers=5)
        end_time = time.time()
        
        # Verify results
        self.assertEqual(len(results), 5)
        self.assertTrue(all(result["success"] for result in results))
        
        # Verify that processing was actually parallel (should be faster than sequential)
        # Sequential would take ~0.5 seconds, parallel should be closer to 0.1 seconds
        processing_time = end_time - start_time
        # Allow some overhead, but it should still be significantly faster than sequential
        self.assertLess(processing_time, 0.3)  # Less than 300ms
        
        # Verify all inputs were processed
        processed_texts = [result["input_text"] for result in results]
        self.assertEqual(set(processed_texts), set(text_values))
    
    def test_process_rows_parallel_with_errors(self):
        """Test parallel processing with some failing tasks."""
        # Create test data with one item that will cause an error
        text_values = [
            "Valid query 1",
            "Valid query 2",
            "ERROR_TRIGGER",  # This will cause an exception
            "Valid query 3"
        ]
        
        # Define a processing function that raises an exception for specific input
        def process_func(text_item):
            if text_item == "ERROR_TRIGGER":
                raise ValueError("Simulated processing error")
            
            return {
                "input_text": text_item,
                "response": f"Response to {text_item}",
                "success": True
            }
        
        # Process with parallel execution
        results = self.processor._process_rows_parallel(text_values, process_func, max_workers=2)
        
        # Verify results
        self.assertEqual(len(results), 4)
        
        # Check successful results
        successful_results = [r for r in results if r.get("success", False)]
        self.assertEqual(len(successful_results), 3)
        
        # Check error result
        error_results = [r for r in results if not r.get("success", True)]
        self.assertEqual(len(error_results), 1)
        self.assertIn("Error processing query", error_results[0]["response"])
    
    @patch('concurrent.futures.ThreadPoolExecutor')
    def test_process_rows_parallel_worker_limit(self, mock_executor_class):
        """Test that the correct number of workers is used."""
        # Mock the ThreadPoolExecutor
        mock_executor = Mock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor
        mock_executor.submit.return_value = Mock()
        
        # Create test data
        text_values = ["Query 1", "Query 2", "Query 3"]
        
        # Define a simple processing function
        def process_func(text_item):
            return {"input_text": text_item, "response": f"Response to {text_item}", "success": True}
        
        # Process with specific worker count
        max_workers = 3
        self.processor._process_rows_parallel(text_values, process_func, max_workers=max_workers)
        
        # Verify ThreadPoolExecutor was called with correct max_workers
        mock_executor_class.assert_called_with(max_workers=max_workers)
        
        # Verify submit was called for each text item
        self.assertEqual(mock_executor.submit.call_count, len(text_values))
    
    def test_process_single_text_with_agent_mocked(self):
        """Test _process_single_text_with_agent with mocked AgentComponent."""
        # Mock the AgentComponent class
        with patch.object(ParallelTextAgentProcessor, 'AgentComponent') as mock_agent_class:
            # Mock the agent instance
            mock_agent = Mock()
            mock_agent_class.return_value = mock_agent
            
            # Mock the message_response method to return a Message
            from langflow.schema.message import Message
            mock_response = Message(text="Mocked response")
            mock_agent.message_response.return_value = mock_response
            
            # Set up processor attributes
            self.processor.custom_instructions = "Test instructions"
            self.processor.agent_llm = "Google Generative AI"
            self.processor.model_name_param = "test-model"
            self.processor.add_current_date_tool = False
            self.processor.n_messages = 100
            
            # Process a single text item
            result = self.processor._process_single_text_with_agent("Test query")
            
            # Verify the result
            self.assertTrue(result["success"])
            self.assertEqual(result["input_text"], "Test query")
            self.assertEqual(result["response"], "Mocked response")
            
            # Verify agent was configured correctly
            self.assertEqual(mock_agent.system_prompt, "Test instructions")
            self.assertEqual(mock_agent.agent_llm, "Google Generative AI")
            self.assertEqual(mock_agent.model_name, "test-model")
            
            # Verify message_response was called
            mock_agent.message_response.assert_called_once()


if __name__ == "__main__":
    print("Testing parallel processing functionality")
    print("=" * 50)
    
    # Run the tests
    unittest.main(verbosity=2)