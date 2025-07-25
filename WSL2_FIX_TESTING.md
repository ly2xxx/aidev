# WSL2 Gemini CLI Fix - Manual Testing Guide

## Issue Fixed
The original `server.py` was failing with `❌ Error: [WinError 2] The system cannot find the file specified` when called from Windows 11 Claude Desktop into WSL2 Ubuntu environment.

## Root Cause
- Basic `subprocess.run(["gemini", ...])` calls couldn't find the gemini CLI
- Gemini is installed via npm at `/home/user/.npm-global/bin/gemini`
- Python subprocess didn't have proper WSL2 environment and PATH setup
- Missing error handling and fallback mechanisms

## Fix Applied
Created robust `run_gemini_command()` wrapper function with:

1. **Proper WSL2 Environment Setup**:
   - Adds `/home/user/.npm-global/bin` to PATH
   - Includes multiple fallback paths
   - Preserves existing environment variables

2. **Multiple Executable Location Detection**:
   - `/home/user/.npm-global/bin/gemini` (primary)
   - `/usr/local/bin/gemini`
   - `/usr/bin/gemini`
   - `~/.npm-global/bin/gemini`
   - Uses `shutil.which()` as fallback

3. **Robust Error Handling**:
   - Comprehensive logging
   - Detailed error messages
   - Timeout management
   - Graceful fallbacks

4. **Startup Verification**:
   - Tests gemini CLI availability on server startup
   - Logs version information
   - Provides early error detection

## Manual Testing Instructions

### Step 1: Test in WSL2 Ubuntu
```bash
# Navigate to the repository
cd /path/to/aidev

# Switch to the fix branch
git checkout fix-gemini-wsl2-subprocess-error

# Test the gemini CLI directly first
which gemini  # Should show /home/user/.npm-global/bin/gemini
gemini --version  # Should show version 0.1.9

# Run the test script
python3 test_gemini_fix.py
```

### Step 2: Expected Test Results
The test script should show:
```
✅ Successfully imported run_gemini_command from server.py
✅ SUCCESS: Gemini version: 0.1.9
✅ SUCCESS: Help command executed successfully
✅ SUCCESS: Prompt execution completed
🎉 ALL TESTS PASSED!
```

### Step 3: Integration Test with Claude Desktop
1. Start the fixed MCP server in WSL2:
   ```bash
   cd gemini-qa-agent
   python3 server.py
   ```

2. Configure Claude Desktop MCP to use the server

3. Test gemini-qa-agent tools from Claude Desktop:
   - Use ask_gemini tool with a simple prompt
   - Should no longer see "WinError 2"
   - Should receive proper responses from Gemini CLI

## Changes Made

### Before (Broken):
```python
result = subprocess.run(
    ["gemini", "--prompt", prompt], 
    capture_output=True, 
    text=True, 
    timeout=90
)
```

### After (Fixed):
```python
def run_gemini_command(args: List[str], working_dir: str = None, timeout: int = 120):
    # Proper WSL2 environment setup
    env = os.environ.copy()
    env['PATH'] = '/home/user/.npm-global/bin:' + env.get('PATH', '')
    
    # Multiple location detection
    gemini_locations = [
        '/home/user/.npm-global/bin/gemini',
        '/usr/local/bin/gemini',
        # ... more fallbacks
    ]
    
    # Find working executable
    gemini_path = None
    for location in gemini_locations:
        if location and os.path.exists(location) and os.access(location, os.X_OK):
            gemini_path = location
            break
    
    # Execute with proper environment
    result = subprocess.run(
        [gemini_path] + args,
        capture_output=True,
        text=True,
        env=env,
        cwd=working_dir,
        timeout=timeout,
        check=False
    )
    
    return result

# Usage
result = run_gemini_command(["--prompt", prompt], timeout=90)
```

## Files Modified
- `gemini-qa-agent/server.py` - Main fix implementation
- `test_gemini_fix.py` - Test script to verify fix

## Verification Checklist
- [ ] gemini CLI accessible in WSL2: `which gemini`
- [ ] Test script passes: `python3 test_gemini_fix.py`
- [ ] MCP server starts without errors
- [ ] Claude Desktop can call gemini-qa-agent tools
- [ ] No more "WinError 2" messages
- [ ] Gemini responses work correctly

## Troubleshooting
If tests still fail:

1. **Check gemini installation**:
   ```bash
   npm list -g @google/gemini-cli
   ls -la /home/user/.npm-global/bin/gemini
   ```

2. **Verify PATH setup**:
   ```bash
   echo $PATH | grep npm-global
   ```

3. **Check permissions**:
   ```bash
   ls -la /home/user/.npm-global/bin/gemini
   chmod +x /home/user/.npm-global/bin/gemini
   ```

4. **Test subprocess directly**:
   ```python
   import subprocess
   result = subprocess.run(['/home/user/.npm-global/bin/gemini', '--version'], 
                          capture_output=True, text=True)
   print(result.stdout)
   ```

This fix should resolve the WSL2 subprocess issue and make gemini-qa-agent fully functional from Windows 11 Claude Desktop.
