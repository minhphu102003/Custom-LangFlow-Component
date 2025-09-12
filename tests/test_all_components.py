"""
Comprehensive test script for all custom components.
"""

import sys
import os
import time
import json

# Add the parent directory to Python path to make imports work correctly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

print("Testing All Custom Components")
print("=" * 40)

# Test all components
components_to_test = [
    "SimpleDataFrameProcessor",
    "ParallelDataFrameProcessor",
    "IntegratedParallelProcessor",
    "ParallelQueryProcessor",
    "ParallelAgentProcessor"
]

for component_name in components_to_test:
    try:
        # Dynamically import the component
        if component_name == "SimpleDataFrameProcessor":
            from processors.simple_dataframe_processor import SimpleDataFrameProcessor
            component_class = SimpleDataFrameProcessor
        elif component_name == "ParallelDataFrameProcessor":
            from processors.parallel_dataframe_processor import ParallelDataFrameProcessor
            component_class = ParallelDataFrameProcessor
        elif component_name == "IntegratedParallelProcessor":
            from processors.integrated_parallel_processor import IntegratedParallelProcessor
            component_class = IntegratedParallelProcessor
        elif component_name == "ParallelQueryProcessor":
            from processors.parallel_query_processor import ParallelQueryProcessor
            component_class = ParallelQueryProcessor
        elif component_name == "ParallelAgentProcessor":
            from processors.parallel_agent_processor import ParallelAgentProcessor
            component_class = ParallelAgentProcessor
        else:
            continue
            
        print(f"\n✓ {component_name} imported successfully")
        
        # Create an instance
        component = component_class()
        print(f"  Created instance of {component_name}")
        
    except Exception as e:
        print(f"✗ Failed to import or instantiate {component_name}: {e}")

# Test a few key components with sample data
print("\n" + "=" * 40)
print("Running functional tests...")

# Test Simple DataFrame Processor
print("\nTesting SimpleDataFrameProcessor...")
try:
    from processors.simple_dataframe_processor import SimpleDataFrameProcessor
    processor = SimpleDataFrameProcessor()
    
    test_df = {
        "data": [
            {"text": "What is AI?"},
            {"text": "How does ML work?"},
            {"text": "What are neural networks?"}
        ]
    }
    
    processor.dataframe_input = test_df
    results = processor.build_processed_results()
    detailed = processor.build_detailed_results()
    
    print("  Processed results:", results[:100] + "..." if len(results) > 100 else results)
    detailed_data = detailed.data if hasattr(detailed, 'data') else detailed
    print("  Total processed:", detailed_data.get('total_processed', 'N/A'))
    print("  ✓ SimpleDataFrameProcessor functional test passed")
except Exception as e:
    print(f"  ✗ SimpleDataFrameProcessor functional test failed: {e}")

# Test Parallel Agent Processor
print("\nTesting ParallelAgentProcessor...")
try:
    from processors.parallel_agent_processor import ParallelAgentProcessor
    processor = ParallelAgentProcessor()
    
    test_df = {
        "data": [
            {"text": "What is AI?"},
            {"text": "How does ML work?"},
            {"text": "What are neural networks?"},
            {"text": "Explain deep learning"},
            {"text": "What is NLP?"}
        ]
    }
    
    processor.dataframe_input = test_df
    processor.agent_count = "2"
    # Not setting max_workers to test automatic determination based on DataFrame size
    
    start_time = time.time()
    results = processor.build_processed_results()
    end_time = time.time()
    
    detailed = processor.build_detailed_results()
    detailed_data = detailed.data if hasattr(detailed, 'data') else detailed
    
    print(f"  Processed in {end_time - start_time:.2f} seconds")
    print("  Processed results length:", len(results))
    print("  Total processed:", detailed_data.get('total_processed', 'N/A'))
    print("  ✓ ParallelAgentProcessor functional test passed")
except Exception as e:
    print(f"  ✗ ParallelAgentProcessor functional test failed: {e}")

print("\n" + "=" * 40)
print("All tests completed.")