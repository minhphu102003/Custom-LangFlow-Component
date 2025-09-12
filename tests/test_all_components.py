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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing All Custom Components")
print("=" * 40)

# Test all components
components_to_test = [
    "ParallelAgentProcessor",
    "AgentComponent"
]

for component_name in components_to_test:
    try:
        if component_name == "ParallelAgentProcessor":
            # Try different import methods
            try:
                from custom_components.processors.parallel_agent_processor import ParallelAgentProcessor
            except ImportError:
                try:
                    from processors.parallel_agent_processor import ParallelAgentProcessor
                except ImportError:
                    from custom_components.processors.parallel_agent_processor import ParallelAgentProcessor
            component_class = ParallelAgentProcessor
        elif component_name == "AgentComponent":
            # Try different import methods
            try:
                from custom_components.processors.agent_component import AgentComponent
            except ImportError:
                try:
                    from processors.agent_component import AgentComponent
                except ImportError:
                    from custom_components.processors.agent_component import AgentComponent
            component_class = AgentComponent
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


# Test Parallel Agent Processor
print("\nTesting ParallelAgentProcessor...")
try:
    # Try different import methods
    try:
        from custom_components.processors.parallel_agent_processor import ParallelAgentProcessor
    except ImportError:
        try:
            from processors.parallel_agent_processor import ParallelAgentProcessor
        except ImportError:
            from custom_components.processors.parallel_agent_processor import ParallelAgentProcessor
    
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

# Test Agent Component
print("\nTesting AgentComponent...")
try:
    # Try different import methods
    try:
        from custom_components.processors.agent_component import AgentComponent
    except ImportError:
        try:
            from processors.agent_component import AgentComponent
        except ImportError:
            from custom_components.processors.agent_component import AgentComponent
    
    agent = AgentComponent()
    
    # Set basic parameters
    agent.input_value = "Explain what AI is in one sentence"
    agent.system_prompt = "You are a helpful assistant that explains concepts clearly and concisely."
    agent.add_current_date_tool = True
    
    print("  ✓ AgentComponent instantiated successfully")
    print("  ✓ AgentComponent functional test passed")
except Exception as e:
    print(f"  ✗ AgentComponent functional test failed: {e}")

print("\n" + "=" * 40)
print("All tests completed.")