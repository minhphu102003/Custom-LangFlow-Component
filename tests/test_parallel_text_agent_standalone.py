"""
Test script for standalone ParallelTextAgentProcessor component.
"""

import sys
import os

# Add the parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

print("Testing Standalone ParallelTextAgentProcessor Component")
print("=" * 55)

try:
    # Import the ParallelTextAgentProcessor
    from processors.parallel_text_agent import ParallelTextAgentProcessor, Message
    
    # Create an instance
    processor = ParallelTextAgentProcessor()
    print("✓ ParallelTextAgentProcessor instantiated successfully")
    
    # Test with list of strings
    print("\nTesting with list of strings:")
    test_inputs = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "Explain neural networks"
    ]
    
    processor.text_inputs = test_inputs
    processor.agent_prompt = "You are a helpful AI assistant that explains concepts clearly and concisely."
    processor.agent_llm = "Google Generative AI"
    processor.model_name_param = "gemini-2.0-flash-001"
    
    # Test processed results
    results = processor.build_processed_results()
    print(f"✓ Processed results (type: {type(results).__name__}):")
    print(f"  Length: {len(str(results))} characters")
    print(f"  Preview: {str(results)[:100]}...")
    
    # Test detailed results
    detailed = processor.build_detailed_results()
    print(f"\n✓ Detailed results (type: {type(detailed).__name__}):")
    if hasattr(detailed, 'data'):
        print(f"  Data keys: {list(detailed.data.keys()) if isinstance(detailed.data, dict) else 'Not a dict'}")
        print(f"  Total processed: {detailed.data.get('total_processed', 0)}")
    
    # Test message results
    messages = processor.build_message_results()
    print(f"\n✓ Message results (type: {type(messages).__name__}):")
    print(f"  Number of messages: {len(messages)}")
    if messages:
        first_message = messages[0]
        if hasattr(first_message, 'text'):
            print(f"  First message preview: {first_message.text[:50]}...")
        else:
            print(f"  First message: {str(first_message)[:50]}...")
    
    # Test with Message objects
    print("\n\nTesting with Message objects:")
    message_inputs = [
        Message(text="What is deep learning?"),
        Message(text="Explain reinforcement learning"),
        Message(text="What is natural language processing?")
    ]
    
    processor.text_inputs = message_inputs
    results = processor.build_processed_results()
    print(f"✓ Processed results with Message inputs:")
    print(f"  Length: {len(str(results))} characters")
    
    print("\n✓ Standalone ParallelTextAgentProcessor component test completed")
    
except Exception as e:
    print(f"✗ Failed to test ParallelTextAgentProcessor: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 55)
print("Standalone ParallelTextAgentProcessor component test completed.")