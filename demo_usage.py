"""
Demo script showing how to use the custom components programmatically.
"""

import sys
import os
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the custom components
from processors.simple_dataframe_processor import SimpleDataFrameProcessor
from processors.parallel_dataframe_processor import ParallelDataFrameProcessor
from processors.integrated_parallel_processor import IntegratedParallelProcessor
from processors.parallel_query_processor import ParallelQueryProcessor

def create_sample_data():
    """Create sample data for processing."""
    return {
        "data": [
            {"text": "What is artificial intelligence?"},
            {"text": "How does machine learning work?"},
            {"text": "What are neural networks?"},
            {"text": "Explain deep learning"},
            {"text": "What is natural language processing?"}
        ]
    }

def demo_simple_processor():
    """Demonstrate the simple DataFrame processor."""
    print("=== Simple DataFrame Processor Demo ===")
    
    # Create processor instance
    processor = SimpleDataFrameProcessor()
    
    # Set input data
    processor.dataframe_input = create_sample_data()
    
    # Process and get results
    results = processor.build_processed_results()
    detailed_results = processor.build_detailed_results()
    
    print("Processed Results:")
    print(results)
    print("\nDetailed Results:")
    print(json.dumps(detailed_results.data, indent=2))

def demo_parallel_processor():
    """Demonstrate the parallel DataFrame processor."""
    print("\n=== Parallel DataFrame Processor Demo ===")
    
    # Create processor instance
    processor = ParallelDataFrameProcessor()
    
    # Set input data
    processor.dataframe_input = create_sample_data()
    processor.max_workers = "3"
    
    # Process and get results
    results = processor.build_processed_results()
    detailed_results = processor.build_detailed_results()
    
    print("Processed Results:")
    print(results)
    print("\nDetailed Results:")
    print(json.dumps(detailed_results.data, indent=2))

def demo_integrated_processor():
    """Demonstrate the integrated parallel processor."""
    print("\n=== Integrated Parallel Processor Demo ===")
    
    # Create processor instance
    processor = IntegratedParallelProcessor()
    
    # Set input data
    processor.dataframe_input = create_sample_data()
    processor.max_workers = "3"
    
    # Process and get results
    results = processor.build_processed_results()
    detailed_results = processor.build_detailed_results()
    
    print("Processed Results:")
    print(results)
    print("\nDetailed Results:")
    print(json.dumps(detailed_results.data, indent=2))

def demo_query_processor():
    """Demonstrate the parallel query processor."""
    print("\n=== Parallel Query Processor Demo ===")
    
    # Create processor instance
    processor = ParallelQueryProcessor()
    
    # Set input data
    processor.dataframe_input = create_sample_data()
    processor.max_workers = "3"
    
    # Process and get results
    results = processor.build_combined_results()
    detailed_results = processor.build_detailed_results()
    
    print("Combined Results:")
    print(results)
    print("\nDetailed Results:")
    print(json.dumps(detailed_results.data, indent=2))

if __name__ == "__main__":
    print("Custom Components Demo")
    print("=" * 30)
    
    try:
        demo_simple_processor()
        demo_parallel_processor()
        demo_integrated_processor()
        demo_query_processor()
        
        print("\n" + "=" * 30)
        print("Demo completed successfully!")
        
    except Exception as e:
        print(f"Error during demo: {e}")
        import traceback
        traceback.print_exc()