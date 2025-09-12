"""
Script to verify that all custom components can be imported correctly.
"""

import sys
import os

# Add the parent directory to Python path to make imports work correctly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

def test_import(component_name, import_path):
    """Test if a component can be imported."""
    try:
        __import__(import_path)
        print(f"✓ {component_name} imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import {component_name}: {e}")
        return False

print("Verifying Custom Component Installation")
print("=" * 40)

# List of components to test
components = [
    ("ParallelAgentProcessor", "processors.parallel_agent_processor"),
    ("BaseProcessor", "processors.base_processor"),
    ("utils", "utils.utils"),
    ("result_processing", "utils.result_processing")
]

# Test imports
successful = 0
total = len(components)

for component_name, import_path in components:
    if test_import(component_name, import_path):
        successful += 1

print(f"\nImport Summary: {successful}/{total} components imported successfully")

if successful == total:
    print("✓ All components installed correctly!")
else:
    print("⚠ Some components failed to import. Check the errors above.")

print("\nInstallation verification completed.")