"""
Test script for the Parallel DataFrame Processor component.
"""

import sys
import os
import time

# Add the parent directory to Python path to make imports work correctly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

def test_parallel_processor():
    """Test the Parallel DataFrame Processor component."""
    print("Testing Parallel DataFrame Processor")
    print("=" * 40)
    
    try:
        from processors.parallel_dataframe_processor import ParallelDataFrameProcessor
        
        # Create an instance
        processor = ParallelDataFrameProcessor()
        print("✓ ParallelDataFrameProcessor imported and instantiated successfully")
        
        # Set up test data
        test_data = {
            "data": [
                {"text": "What is artificial intelligence?"},
                {"text": "How does machine learning work?"},
                {"text": "What are neural networks?"},
                {"text": "Explain deep learning"},
                {"text": "What is natural language processing?"}
            ]
        }
        
        processor.dataframe_input = test_data
        processor.max_workers = "3"  # Test with 3 workers
        
        # Process the data
        start_time = time.time()
        results = processor.build_processed_results()
        end_time = time.time()
        
        print(f"  Processing completed in {end_time - start_time:.2f} seconds")
        print(f"  Results length: {len(results)} characters")
        print(f"  Sample result: {results[:100]}...")
        
        # Test detailed results
        detailed_results = processor.build_detailed_results()
        detailed_data = detailed_results.data if hasattr(detailed_results, 'data') else detailed_results
        
        print(f"  Total processed: {detailed_data.get('total_processed', 'N/A')}")
        print(f"  Success count: {detailed_data.get('success_count', 'N/A')}")
        print(f"  Error count: {detailed_data.get('error_count', 'N/A')}")
        
        print("✓ Parallel DataFrame Processor test passed")
        return True
        
    except Exception as e:
        print(f"✗ Parallel DataFrame Processor test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_parallel_processor()
    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed!")