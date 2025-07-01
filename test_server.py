#!/usr/bin/env python3

import subprocess
import sys
import time

def test_server():
    """Test the MCP server functionality"""
    print("Testing MCP server...")
    
    # Test calculator imports
    try:
        from tools.calculator import add, subtract, multiply, divide
        print("✓ Calculator tools imported successfully")
        print(f"  add(5, 3) = {add(5, 3)}")
        print(f"  subtract(10, 4) = {subtract(10, 4)}")
        print(f"  multiply(6, 7) = {multiply(6, 7)}")
        print(f"  divide(15, 3) = {divide(15, 3)}")
    except Exception as e:
        print(f"✗ Calculator tools error: {e}")
        return False
    
    # Test prompt import
    try:
        from prompts.pirate_talk import get_pirate_prompt
        result = get_pirate_prompt("Hello there!")
        print("✓ Pirate talk prompt imported successfully")
        print(f"  Template preview: {result[:100]}...")
    except Exception as e:
        print(f"✗ Pirate talk prompt error: {e}")
        return False
    
    # Test server import
    try:
        import server
        print("✓ Server module imported successfully")
    except Exception as e:
        print(f"✗ Server import error: {e}")
        return False
    
    print("\n✓ All tests passed! Server should work with Inspector.")
    return True

if __name__ == "__main__":
    if test_server():
        print("\nTo run with Inspector:")
        print("DANGEROUSLY_OMIT_AUTH=true npx @modelcontextprotocol/inspector python3 server.py --stdio")
        print("\nThen open: http://127.0.0.1:6274")
    else:
        print("\nPlease fix the errors above before running Inspector.")
        sys.exit(1)