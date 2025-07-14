# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing MCP Servers
- `python3 test_servers.py` - Test both MCP servers for functionality
- `python test_servers.py` - Windows alternative test command

### Making Servers Executable
```bash
chmod +x claude-code-developer/server.py
chmod +x gemini-qa-agent/server.py
```

### Dependencies
- Install MCP library: `pip install --break-system-packages mcp` (Linux/WSL)
- For Windows virtual environment: `pip install mcp`
- Install python-dotenv: `pip install python-dotenv`

### Environment Setup
- Create `.env` file in the aidev directory (`/mnt/h/code/yl/aidev/.env`) with:
  ```
  # Claude Code uses your Claude account's shared authentication token
  # No separate API key needed - just ensure you're logged into Claude
  
  # Gemini API Key for gemini-qa-agent MCP server  
  GEMINI_API_KEY=your_gemini_api_key_here
  ```
- **Claude Code Authentication**: Uses your Claude account's shared authentication token automatically
- **Gemini Authentication**: Requires API key from Google AI Studio
- The `.env` file is excluded from version control via `.gitignore`

## Architecture Overview

This is an **MCP-based development crew system** that implements two specialized MCP (Model Context Protocol) servers for coordinated AI development workflows.

### Core Components

**Claude Code Developer Agent (`claude-code-developer/server.py`)**:
- MCP server that wraps Claude Code CLI functionality
- Handles code generation, file analysis, feature branch creation, and URL content analysis
- Tools: `generate_code`, `analyze_file`, `create_feature_branch`, `analyze_url_content`, `ask_claude`
- Uses subprocess calls to execute Claude Code CLI commands with structured prompts
- Uses Claude account's shared authentication token (no separate API key needed)

**Gemini QA Agent (`gemini-qa-agent/server.py`)**:
- MCP server that wraps Gemini CLI for quality assurance tasks
- Provides comprehensive code review, test generation, security audits, and performance analysis
- Tools: `review_code`, `generate_tests`, `security_audit`, `performance_analysis`, `code_quality_report`, `ask_gemini`
- Uses Gemini CLI for AI-powered code analysis and testing
- Automatically loads GEMINI_API_KEY from aidev directory `.env` file

**Test Infrastructure (`test_servers.py`)**:
- Automated testing script for verifying MCP server functionality
- Cross-platform compatibility (handles both Linux/WSL and Windows Python commands)
- Validates server startup and basic operation

### Configuration Files

The repository includes multiple Claude Desktop configuration files for different environments:
- `claude_desktop_config.json` - Linux/WSL configuration
- `windows_claude_desktop_config.json` - Windows system Python
- `windows_venv_claude_desktop_config.json` - Windows virtual environment
- `wsl_claude_desktop_config.json` - Windows using WSL

### Integration Patterns

**Workflow Orchestration**:
- Claude Desktop acts as coordinator between the two MCP agents
- Developer agent handles code generation and implementation
- QA agent provides review, testing, and quality assurance
- Git workflow integration for branch management and commits

**Tool Communication**:
- Both servers follow standard MCP protocol with `@server.list_tools()` and `@server.call_tool()` decorators
- Structured input schemas for type-safe tool invocation
- Comprehensive error handling and timeout management
- Cross-platform subprocess execution with proper command selection

### Key Technical Details

- MCP servers run as separate Python processes communicating via stdio
- Timeout management: code generation (180s), analysis (60-120s), security audits (45-60s)
- File content size limits for processing (10KB for URL content, 2KB for config files)
- Automatic test file generation with framework-specific naming conventions
- Git branch naming sanitization using regex patterns
- Platform detection for GitHub/GitLab CLI integration

### Development Workflow Templates

The system supports coordinated workflows including:
- Feature development from description or URL analysis
- Code review and improvement cycles
- Security auditing and compliance checking
- Test generation and quality assurance
- Git workflow management and merge request creation