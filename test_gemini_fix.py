#!/usr/bin/env python3
"""
Test script to verify the WSL2 gemini CLI fix
"""

import sys
import os
import logging

# Add the gemini-qa-agent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gemini-qa-agent'))

try:
    from server import run_gemini_command
    print("✅ Successfully imported run_gemini_command from server.py")
except ImportError as e:
    print(f"❌ Failed to import run_gemini_command: {e}")
    sys.exit(1)

def test_gemini_cli():
    """Test the fixed gemini CLI wrapper function"""
    
    print("🧪 Testing WSL2 Gemini CLI Fix")
    print("=" * 50)
    
    # Test 1: Version check
    print("\n📋 Test 1: Gemini CLI Version Check")
    try:
        result = run_gemini_command(["--version"], timeout=15)
        if result.returncode == 0:
            print(f"✅ SUCCESS: Gemini version: {result.stdout.strip()}")
        else:
            print(f"❌ FAILED: Return code {result.returncode}")
            print(f"   stderr: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        return False
    
    # Test 2: Help output
    print("\n📋 Test 2: Gemini CLI Help")
    try:
        result = run_gemini_command(["--help"], timeout=15)
        if result.returncode == 0:
            print("✅ SUCCESS: Help command executed successfully")
            # Check if we got expected help output
            if "Options:" in result.stdout and "--prompt" in result.stdout:
                print("✅ SUCCESS: Help output contains expected content")
            else:
                print("⚠️  WARNING: Help output format might be different")
        else:
            print(f"❌ FAILED: Return code {result.returncode}")
            print(f"   stderr: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        return False
    
    # Test 3: Simple prompt execution
    print("\n📋 Test 3: Simple Prompt Execution")
    try:
        test_prompt = "Hello! Please respond with 'WSL2 Gemini CLI is working correctly' to confirm the fix is successful."
        result = run_gemini_command(["--prompt", test_prompt], timeout=30)
        if result.returncode == 0:
            print("✅ SUCCESS: Prompt execution completed")
            print(f"   Response preview: {result.stdout[:100]}...")
            # Check if we got a reasonable response
            if len(result.stdout.strip()) > 10:
                print("✅ SUCCESS: Received substantial response from Gemini")
            else:
                print("⚠️  WARNING: Response seems too short")
        else:
            print(f"❌ FAILED: Return code {result.returncode}")
            print(f"   stderr: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        return False
    
    return True

def test_environment_info():
    """Display environment information for debugging"""
    
    print("\n🔍 Environment Information")
    print("=" * 50)
    
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"PATH: {os.environ.get('PATH', 'NOT SET')}")
    print(f"USER: {os.environ.get('USER', 'NOT SET')}")
    print(f"HOME: {os.environ.get('HOME', 'NOT SET')}")
    
    # Check for gemini CLI
    import shutil
    gemini_path = shutil.which('gemini')
    print(f"Gemini CLI found at: {gemini_path}")
    
    # Check specific locations
    locations_to_check = [
        '/home/user/.npm-global/bin/gemini',
        '/usr/local/bin/gemini',
        '/usr/bin/gemini'
    ]
    
    print("\nChecking specific gemini locations:")
    for location in locations_to_check:
        exists = os.path.exists(location)
        executable = os.access(location, os.X_OK) if exists else False
        print(f"  {location}: {'✅ exists' if exists else '❌ missing'} {'& executable' if executable else ''}")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("🚀 WSL2 Gemini CLI Fix Test Suite")
    print("Testing the fixed server.py implementation")
    
    # Show environment info first
    test_environment_info()
    
    # Run the main tests
    success = test_gemini_cli()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ The WSL2 subprocess fix appears to be working correctly.")
        print("✅ gemini-qa-agent should now work from Windows 11 Claude Desktop.")
    else:
        print("❌ SOME TESTS FAILED!")
        print("❌ The fix may need additional adjustments.")
        print("❌ Check the error messages above for details.")
    
    print("\n📝 Next steps:")
    print("1. If tests passed: Create pull request")
    print("2. If tests failed: Debug and iterate on the fix")
    print("3. Test the full MCP integration with Claude Desktop")
