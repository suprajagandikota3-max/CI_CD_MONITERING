#!/usr/bin/env python3
"""
Test script to verify imports work without running Streamlit app
"""

try:
    import streamlit
    print("✅ Streamlit works")
    
    import wikipedia
    print("✅ Wikipedia works")
    
    # Test basic Wikipedia functionality
    wikipedia.set_lang("en")
    print("✅ Wikipedia configuration works")
    
    print("✅ All imports and basic functionality successful!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)
except Exception as e:
    print(f"❌ Other error: {e}")
    exit(1)
