"""
Test script for TextExtractor component.
"""

import sys
import os

# Add the parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

print("Testing TextExtractor Component")
print("=" * 40)

try:
    # Import the TextExtractor
    try:
        from processors.text_extractor import TextExtractor
    except ImportError:
        try:
            from custom_components.processors.text_extractor import TextExtractor
        except ImportError:
            from custom_components.processors.text_extractor import TextExtractor
    
    # Create an instance
    extractor = TextExtractor()
    print("✓ TextExtractor instantiated successfully")
    
    # Test with dictionary format (strings output)
    print("\nTesting with dictionary format (strings output):")
    test_data = {
        "data": [
            {"text": "First text sample"},
            {"text": "Second text sample"},
            {"text": "Third text sample"}
        ]
    }
    
    extractor.data = test_data
    extractor.output_as_messages = False
    result = extractor.extract_text()
    print(f"✓ Extracted {len(result)} text items:")
    for i, text in enumerate(result):
        print(f"  {i+1}. {text}")
    
    # Test with dictionary format (messages output)
    print("\nTesting with dictionary format (messages output):")
    extractor.output_as_messages = True
    result_messages = extractor.extract_text()
    print(f"✓ Extracted {len(result_messages)} message items:")
    for i, msg in enumerate(result_messages):
        # Check if it's a Message object
        if hasattr(msg, 'text'):
            print(f"  {i+1}. {msg.text} (Message object)")
        else:
            print(f"  {i+1}. {msg}")
    
    # Test with list format (strings output)
    print("\nTesting with list format (strings output):")
    list_data = ["Item 1", "Item 2", "Item 3"]
    extractor.data = list_data
    extractor.output_as_messages = False
    result = extractor.extract_text()
    print(f"✓ Extracted {len(result)} text items:")
    for i, text in enumerate(result):
        print(f"  {i+1}. {text}")
    
    # Test with list format (messages output)
    print("\nTesting with list format (messages output):")
    extractor.output_as_messages = True
    result_messages = extractor.extract_text()
    print(f"✓ Extracted {len(result_messages)} message items:")
    for i, msg in enumerate(result_messages):
        # Check if it's a Message object
        if hasattr(msg, 'text'):
            print(f"  {i+1}. {msg.text} (Message object)")
        else:
            print(f"  {i+1}. {msg}")
    
    # Test with single string (strings output)
    print("\nTesting with single string (strings output):")
    string_data = "Single text item"
    extractor.data = string_data
    extractor.output_as_messages = False
    result = extractor.extract_text()
    print(f"✓ Extracted {len(result)} text items:")
    for i, text in enumerate(result):
        print(f"  {i+1}. {text}")
    
    # Test with single string (messages output)
    print("\nTesting with single string (messages output):")
    extractor.output_as_messages = True
    result_messages = extractor.extract_text()
    print(f"✓ Extracted {len(result_messages)} message items:")
    for i, msg in enumerate(result_messages):
        # Check if it's a Message object
        if hasattr(msg, 'text'):
            print(f"  {i+1}. {msg.text} (Message object)")
        else:
            print(f"  {i+1}. {msg}")
    
    print("\n✓ TextExtractor component test passed")
    
except Exception as e:
    print(f"✗ Failed to test TextExtractor: {e}")

print("\n" + "=" * 40)
print("TextExtractor component test completed.")