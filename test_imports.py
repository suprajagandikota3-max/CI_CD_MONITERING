#!/usr/bin/env python3
"""
Simple import test for CI/CD
"""

try:
    import streamlit
    print("✅ Streamlit works")
    
    import wikipedia
    print("✅ Wikipedia works")
    
    import auth
    print("✅ Auth system works")
    
    # Test main imports without executing
    import main
    print("✅ Main app imports work")
    
    print("🎉 All imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    exit(1)
