# Robust CI/CD Tests 🚀

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
    
    try:
        # Test the function
        hashed = make_password("test123")
        assert len(hashed) == 64  # SHA256 should be 64 chars
        assert make_password("same") == make_password("same")
        assert make_password("diff") != make_password("different")
        
        print("✅ Password hashing works correctly!")
        return True
    except Exception as e:
        print(f"❌ Password test failed: {e}")
        return False

def test_file_structure():
    """Check if required files exist"""
    import os
    
    required_files = ['main.py', 'auth.py', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present!")
        return True

# ✅✅✅ CORRECTED LINE - TWO UNDERSCORES! ✅✅✅
if __name__ == "__main__":
    print("🧪 Starting CI/CD Tests...")
    
    tests = [
        test_imports(),
        test_password_hashing(), 
        test_file_structure()
    ]
    
    if all(tests):
        print("🎉 ALL TESTS PASSED! Your app is ready! 🚀")
    else:
        print("❌ Some tests failed. Check the errors above.")
        exit(1)
