#!/usr/bin/env python3
"""
Ultra-simple test for CI/CD troubleshooting
"""

try:
    print("🧪 Running ultra-simple tests...")
    
    # Basic imports
    import streamlit
    print("✅ Streamlit works")
    
    import wikipedia
    print("✅ Wikipedia works")
    
    import pytest
    print("✅ Pytest works")
    
    # Check main file exists and has valid syntax
    with open('main.py', 'r') as f:
        content = f.read()
    compile(content, 'main.py', 'exec')
    print("✅ main.py has valid syntax")
    
    print("🎉 ALL BASIC TESTS PASSED!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    exit(1)
