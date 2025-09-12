"""
Test script for ParallelAgentProcessor with Gemini integration.
"""

import sys
import os
import time

# Add the parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ Environment variables loaded successfully")
except ImportError:
    print("! python-dotenv not installed. Using default values.")

print("Testing ParallelAgentProcessor with Gemini")
print("=" * 40)

try:
    # Import the ParallelAgentProcessor
    from processors.parallel_agent_processor import ParallelAgentProcessor
    
    # Create an instance of ParallelAgentProcessor
    processor = ParallelAgentProcessor()
    
    # Create test data
    test_df = {
        "data": [
            {"text": "Explain what artificial intelligence is."},
            {"text": "What is machine learning?"},
            {"text": "How do neural networks work?"},
            {"text": "What is deep learning?"},
            {"text": "What is natural language processing?"}
        ]
    }
    
    # Set the input data
    processor.dataframe_input = test_df
    
    # Set system prompt for all agents
    processor.system_prompt = "You are a helpful AI assistant that explains concepts clearly and concisely. Keep your answers brief but informative."
    
    # Set model configuration for all agents (this will be used in the parallel processor)
    processor.model_name = "gemini-2.0-flash-001"
    processor.agent_llm = "Google Generative AI"
    
    print("✓ ParallelAgentProcessor instantiated successfully")
    print(f"  Number of test queries: {len(test_df['data'])}")
    print(f"  System prompt: {processor.system_prompt}")
    
    # Check if API key is set
    google_api_key = os.getenv("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY_HERE")
    print(f"  API Key: {google_api_key}")  # Debug: Print the API key
    if google_api_key == "YOUR_GOOGLE_API_KEY_HERE":
        print("\n! Warning: Google API key not found in environment variables")
        print("  Please create a .env file with your GOOGLE_API_KEY")
    else:
        print("✓ Google API key loaded from environment")
    
    # Test the parallel processor
    try:
        start_time = time.time()
        results = processor.build_processed_results()
        end_time = time.time()
        
        # Results should be a string, not a Message object
        results_text = str(results)
        
        detailed = processor.build_detailed_results()
        detailed_data = detailed.data if hasattr(detailed, 'data') else detailed
        
        print(f"\n✓ Parallel processing completed in {end_time - start_time:.2f} seconds")
        print(f"  Processed results length: {len(results_text)}")
        # Note: The following stats may not be available depending on the implementation of create_detailed_results_data
        if isinstance(detailed_data, dict):
            print(f"  Total processed: {detailed_data.get('total_processed', 'N/A')}")
            print(f"  Successful: {detailed_data.get('successful', 'N/A')}")
            print(f"  Failed: {detailed_data.get('failed', 'N/A')}")
        else:
            print(f"  Detailed data type: {type(detailed_data)}")
        
        # Show a snippet of the results
        print(f"\nSample results (first 200 chars):")
        print(results_text[:200] + "..." if len(results_text) > 200 else results_text)
        
        print("✓ ParallelAgentProcessor with Gemini test passed")
        
    except Exception as e:
        print(f"\n✗ ParallelAgentProcessor test failed: {e}")
        if google_api_key == "YOUR_GOOGLE_API_KEY_HERE":
            print("  Note: This is expected because the Google API key is not configured")
        else:
            print("  Note: Check your API key and network connection")
        
except Exception as e:
    print(f"✗ Failed to import or instantiate ParallelAgentProcessor: {e}")

print("\n" + "=" * 40)
print("ParallelAgentProcessor with Gemini test completed.")