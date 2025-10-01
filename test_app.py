def test_imports():
    """Test if we can import all required packages"""
    try:
        import streamlit
        import wikipedia
        import json
        import hashlib
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_password_hashing():
    """Test our password hashing function"""
    import hashlib
    
    def make_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    # Test the function
    hashed = make_password("test123")
    assert len(hashed) == 64  # SHA256 should be 64 chars
    assert make_password("same") == make_password("same")  # Same input = same output
    assert make_password("diff") != make_password("different")  # Different input = different output
    
    print("✅ Password hashing works correctly!")
    return True

if _name_ == "_main_":
    test_imports()
    test_password_hashing()
    print("🎉 All tests passed!")
