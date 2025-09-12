"""
Test script for AgentComponent with Gemini integration.
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

print("Testing AgentComponent with Gemini")
print("=" * 40)

try:
    # Import the AgentComponent
    from processors.agent_component import AgentComponent
    from langflow.schema.message import Message
    
    # Create an instance of AgentComponent following the exact pattern from parallel_agent_processor.py
    agent = AgentComponent()
    
    # Set parameters for the agent (matching the parallel processor setup exactly)
    agent.system_prompt = "You are a helpful AI assistant that explains concepts clearly and concisely."
    # Create a proper Message object for input_value
    agent.input_value = Message(text="Explain what artificial intelligence is in one paragraph.")
    agent.add_current_date_tool = True
    
    # Set model configuration
    agent.agent_llm = "Google Generative AI"
    agent.model_name = "gemini-2.0-flash-001"
    
    # Set Google API key from environment variable
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if google_api_key:
        agent.api_key = google_api_key
    
    # Mock the get_memory_data method to avoid session_id validation issues
    async def mock_get_memory_data():
        return []
    
    agent.get_memory_data = mock_get_memory_data
    
    # Set required attributes for proper initialization
    agent.session_id = "test_session"
    # Create a mock graph object with session_id using a proper approach
    class MockGraph:
        def __init__(self):
            self.session_id = "test_session"
    
    # Use object.__setattr__ to bypass property restrictions
    object.__setattr__(agent, 'graph', MockGraph())
    
    # Initialize tools as an empty list if not already set
    if not hasattr(agent, 'tools') or agent.tools is None:
        agent.tools = []
    # Initialize chat_history as an empty list if not already set
    if not hasattr(agent, 'chat_history'):
        agent.chat_history = []
    # Set default n_messages if not already set
    if not hasattr(agent, 'n_messages'):
        agent.n_messages = 100
    
    # Debug: Print all attributes of the agent
    print("Agent attributes:")
    attrs = [attr for attr in dir(agent) if not attr.startswith('_')]
    for attr in sorted(attrs):
        value = getattr(agent, attr)
        # Only print non-method attributes
        if not callable(value):
            print(f"  {attr}: {value}")
    
    print("\n✓ AgentComponent instantiated successfully")
    print(f"  Provider: {agent.agent_llm}")
    print(f"  Model: {getattr(agent, 'model_name', 'Not set')}")
    print(f"  Input: {agent.input_value.text if hasattr(agent.input_value, 'text') else agent.input_value}")
    
    # Check if API key is set
    print(f"  API Key: {agent.api_key}")
    if agent.api_key == "YOUR_GOOGLE_API_KEY_HERE":
        print("\n! Warning: Google API key not found in environment variables")
        print("  Please create a .env file with your GOOGLE_API_KEY")
    else:
        print("✓ Google API key loaded from environment")
    
    # Test the agent (this will fail if you haven't set up your API key)
    try:
        import asyncio
        # Create a new event loop for this test
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(agent.message_response())
        print(f"\n✓ Agent response received:")
        # Handle both Message objects and plain strings
        if hasattr(response, 'text'):
            print(f"  {response.text}")
            response_text = response.text
        else:
            print(f"  {str(response)}")
            response_text = str(response)
        print("✓ AgentComponent with Gemini test passed")
    except Exception as e:
        print(f"\n✗ AgentComponent test failed: {e}")
        if agent.api_key == "YOUR_GOOGLE_API_KEY_HERE":
            print("  Note: This is expected because the Google API key is not configured")
        else:
            print("  Note: Check your API key and network connection")
        
except Exception as e:
    print(f"✗ Failed to import or instantiate AgentComponent: {e}")

print("\n" + "=" * 40)
print("AgentComponent with Gemini test completed.")