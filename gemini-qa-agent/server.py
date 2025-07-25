#!/usr/bin/env python
"""
Gemini CLI MCP Server - QA Agent
Handles code review, testing, and quality assurance tasks using Gemini CLI
Fixed for WSL2 Ubuntu environment with proper subprocess handling
"""

import asyncio
import json
import subprocess
import sys
import os
import glob
import tempfile
import logging
import shutil
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

server = Server("gemini-qa-agent")

def run_gemini_command(args: List[str], working_dir: str = None, timeout: int = 120) -> subprocess.CompletedProcess:
    """
    Robust Gemini CLI wrapper for WSL2 Ubuntu environment.
    Handles proper PATH setup and environment for npm-installed gemini CLI.
    
    Args:
        args: List of arguments to pass to gemini CLI (excluding 'gemini' itself)
        working_dir: Working directory for the command (defaults to user home)
        timeout: Command timeout in seconds
        
    Returns:
        subprocess.CompletedProcess result
        
    Raises:
        FileNotFoundError: If gemini CLI cannot be found
        subprocess.TimeoutExpired: If command times out
    """
    
    # Ensure we have the user's full environment
    env = os.environ.copy()
    
    # Add npm global bin to PATH - this is crucial for WSL2
    npm_bin_path = '/home/user/.npm-global/bin'
    current_path = env.get('PATH', '')
    if npm_bin_path not in current_path:
        env['PATH'] = npm_bin_path + ':' + current_path
    
    # Also add common npm paths as fallbacks
    additional_paths = [
        '/usr/local/bin',
        '/usr/bin',
        '/bin',
        os.path.expanduser('~/.npm-global/bin'),
        '/home/user/.local/bin'
    ]
    
    for path in additional_paths:
        if path not in env['PATH']:
            env['PATH'] = path + ':' + env['PATH']
    
    # Try multiple possible gemini executable locations
    gemini_locations = [
        '/home/user/.npm-global/bin/gemini',
        '/usr/local/bin/gemini',
        '/usr/bin/gemini',
        os.path.expanduser('~/.npm-global/bin/gemini'),
        shutil.which('gemini')  # Let system find it
    ]
    
    gemini_path = None
    for location in gemini_locations:
        if location and os.path.exists(location) and os.access(location, os.X_OK):
            gemini_path = location
            break
    
    # If still not found, try using shutil.which with updated PATH
    if not gemini_path:
        # Update PATH temporarily to find gemini
        old_path = os.environ.get('PATH', '')
        os.environ['PATH'] = env['PATH']
        try:
            gemini_path = shutil.which('gemini')
        finally:
            os.environ['PATH'] = old_path
    
    if not gemini_path:
        logger.error(f"Gemini CLI not found. Searched locations: {gemini_locations}")
        logger.error(f"Current PATH: {env['PATH']}")
        raise FileNotFoundError("Gemini CLI executable not found. Please ensure it's installed via npm.")
    
    # Set working directory - use user home if not specified
    if working_dir is None:
        working_dir = os.path.expanduser('~')
        if not os.path.exists(working_dir):
            working_dir = '/home/user'
    
    # Build full command with gemini path
    full_cmd = [gemini_path] + args
    
    logger.info(f"Executing Gemini command: {' '.join(full_cmd[:2])}... (truncated for security)")
    logger.info(f"Working directory: {working_dir}")
    logger.info(f"Using gemini at: {gemini_path}")
    
    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            env=env,
            cwd=working_dir,
            timeout=timeout,
            check=False  # Don't raise exception on non-zero exit
        )
        
        logger.info(f"Gemini command completed with return code: {result.returncode}")
        if result.stderr and result.returncode != 0:
            logger.warning(f"Gemini stderr: {result.stderr[:200]}...")
            
        return result
        
    except subprocess.TimeoutExpired as e:
        logger.error(f"Gemini command timed out after {timeout} seconds")
        raise
    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError executing gemini: {e}")
        logger.error(f"Command: {full_cmd}")
        logger.error(f"Working directory: {working_dir}")
        logger.error(f"PATH: {env.get('PATH')}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error executing gemini: {e}")
        raise

@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="review_code",
            description="Review code quality using Gemini CLI",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to code file to review"},
                    "review_type": {"type": "string", "description": "Type of review (security, performance, style, etc.)"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="generate_tests",
            description="Generate test cases for code using Gemini",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_file": {"type": "string", "description": "Source code file to test"},
                    "test_framework": {"type": "string", "description": "Testing framework to use"},
                    "coverage_level": {"type": "string", "description": "Test coverage level (basic, comprehensive)"}
                },
                "required": ["source_file"]
            }
        ),
        Tool(
            name="security_audit",
            description="Perform security audit on code",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_path": {"type": "string", "description": "File or directory path to audit"},
                    "audit_level": {"type": "string", "description": "Audit depth (quick, deep)"}
                },
                "required": ["target_path"]
            }
        ),
        Tool(
            name="performance_analysis",
            description="Analyze code performance and suggest optimizations",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Code file to analyze"},
                    "language": {"type": "string", "description": "Programming language"}
                },
                "required": ["file_path", "language"]
            }
        ),
        Tool(
            name="code_quality_report",
            description="Generate comprehensive code quality report",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "description": "Project directory path"},
                    "include_metrics": {"type": "boolean", "description": "Include quality metrics"}
                },
                "required": ["project_path"]
            }
        ),
        Tool(
            name="ask_gemini",
            description="Ask Gemini directly for QA assistance",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Prompt to send to Gemini"},
                    "include_all_files": {"type": "boolean", "description": "Include all files in context", "default": False}
                },
                "required": ["prompt"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    if name == "review_code":
        return await review_code_handler(arguments)
    elif name == "generate_tests":
        return await generate_tests_handler(arguments)
    elif name == "security_audit":
        return await security_audit_handler(arguments)
    elif name == "performance_analysis":
        return await performance_analysis_handler(arguments)
    elif name == "code_quality_report":
        return await code_quality_report_handler(arguments)
    elif name == "ask_gemini":
        return await ask_gemini_handler(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def review_code_handler(args: Dict[str, Any]) -> List[TextContent]:
    file_path = args["file_path"]
    review_type = args.get("review_type", "general")
    
    try:
        if not os.path.exists(file_path):
            return [TextContent(type="text", text=f"❌ File not found: {file_path}")]
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # Prepare Gemini prompt based on review type
        prompts = {
            "security": f"""Perform a comprehensive security review of this code. Look for:
- Security vulnerabilities and potential exploits
- Input validation issues
- Authentication and authorization flaws
- Data exposure risks
- Injection attack vectors
- Cryptographic issues
- Access control problems

File: {file_path}

Code:
```
{code_content}
```

Provide specific security recommendations and fixes.""",
            
            "performance": f"""Analyze this code for performance issues and optimization opportunities:
- Algorithmic complexity analysis
- Memory usage optimization
- I/O operation efficiency
- Database query optimization
- Caching opportunities
- Resource management
- Scalability concerns

File: {file_path}

Code:
```
{code_content}
```

Provide specific performance improvement recommendations.""",
            
            "style": f"""Review this code for style, readability, and best practices:
- Code organization and structure
- Naming conventions
- Documentation and comments
- Code duplication
- Design patterns usage
- Language-specific best practices
- Maintainability aspects

File: {file_path}

Code:
```
{code_content}
```

Provide specific style and best practice recommendations.""",
            
            "general": f"""Perform a comprehensive code review covering all aspects:
- Code quality and organization
- Security vulnerabilities
- Performance considerations
- Style and best practices
- Maintainability
- Testing considerations
- Documentation quality

File: {file_path}

Code:
```
{code_content}
```

Provide a thorough analysis with specific recommendations for improvement."""
        }
        
        prompt = prompts.get(review_type, prompts["general"])
        
        # Call Gemini CLI using the robust wrapper
        result = run_gemini_command(["--prompt", prompt], timeout=90)
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=f"✅ Code review completed!\n\nFile: {file_path}\nReview Type: {review_type}\n\nGemini Analysis:\n{result.stdout}"
            )]
        else:
            return [TextContent(type="text", text=f"❌ Code review failed: {result.stderr or 'Unknown error'}")]
            
    except Exception as e:
        logger.exception("Error during code review")
        return [TextContent(type="text", text=f"❌ Error during code review: {str(e)}")]

async def generate_tests_handler(args: Dict[str, Any]) -> List[TextContent]:
    source_file = args["source_file"]
    test_framework = args.get("test_framework", "jest")
    coverage_level = args.get("coverage_level", "comprehensive")
    
    try:
        if not os.path.exists(source_file):
            return [TextContent(type="text", text=f"❌ Source file not found: {source_file}")]
        
        with open(source_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        prompt = f"""Generate {coverage_level} test cases for this code using {test_framework}.

Requirements:
- Create thorough unit tests
- Include edge cases and boundary conditions
- Test error scenarios and exception handling
- Include setup and teardown if needed
- Add descriptive test names and comments
- Ensure good test coverage
- Include integration tests where appropriate

Source File: {source_file}
Testing Framework: {test_framework}
Coverage Level: {coverage_level}

Source Code:
```
{source_code}
```

Generate complete, runnable test code with proper structure and organization."""
        
        result = run_gemini_command(["--prompt", prompt], timeout=120)
        
        if result.returncode == 0:
            # Determine test file name based on source file
            base_name = os.path.splitext(os.path.basename(source_file))[0]
            extension = os.path.splitext(source_file)[1]
            
            if extension in ['.js', '.ts', '.jsx', '.tsx']:
                test_file_name = f"{base_name}.test{extension}"
            elif extension == '.py':
                test_file_name = f"test_{base_name}.py"
            elif extension in ['.java']:
                test_file_name = f"{base_name}Test.java"
            else:
                test_file_name = f"{base_name}_test{extension}"
            
            test_file_path = f"./tests/{test_file_name}"
            
            # Create tests directory if it doesn't exist
            os.makedirs("./tests", exist_ok=True)
            
            # Save test file
            try:
                with open(test_file_path, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                
                return [TextContent(
                    type="text",
                    text=f"✅ Test cases generated and saved!\n\nSource: {source_file}\nTest File: {test_file_path}\nFramework: {test_framework}\nCoverage: {coverage_level}\n\nGenerated Tests:\n{result.stdout}"
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"✅ Test cases generated!\n\nSource: {source_file}\nFramework: {test_framework}\nCoverage: {coverage_level}\n\nNote: Could not save to file ({str(e)}), but here are the tests:\n{result.stdout}"
                )]
        else:
            return [TextContent(type="text", text=f"❌ Test generation failed: {result.stderr or 'Unknown error'}")]
            
    except Exception as e:
        logger.exception("Error generating tests")
        return [TextContent(type="text", text=f"❌ Error generating tests: {str(e)}")]

async def security_audit_handler(args: Dict[str, Any]) -> List[TextContent]:
    target_path = args["target_path"]
    audit_level = args.get("audit_level", "quick")
    
    try:
        if os.path.isfile(target_path):
            files_to_audit = [target_path]
        elif os.path.isdir(target_path):
            # Find code files in directory
            patterns = ["**/*.js", "**/*.py", "**/*.ts", "**/*.jsx", "**/*.tsx", "**/*.java", "**/*.php", "**/*.rb", "**/*.go"]
            files_to_audit = []
            for pattern in patterns:
                files_to_audit.extend(glob.glob(os.path.join(target_path, pattern), recursive=True))
        else:
            return [TextContent(type="text", text=f"❌ Path not found: {target_path}")]
        
        # Limit files for audit based on level
        max_files = 20 if audit_level == "deep" else 10
        files_to_audit = files_to_audit[:max_files]
        
        audit_results = []
        for file_path in files_to_audit:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                prompt = f"""Perform a comprehensive security audit of this code file.

Focus on identifying:
- SQL injection vulnerabilities
- Cross-site scripting (XSS) issues
- Authentication bypass possibilities
- Authorization flaws
- Input validation problems
- Data exposure risks
- Cryptographic weaknesses
- File system security issues
- Network security concerns
- Dependency vulnerabilities

File: {file_path}

Code:
```
{content}
```

Provide specific security findings with severity levels and remediation recommendations."""
                
                result = run_gemini_command(["--prompt", prompt], timeout=60)
                
                if result.returncode == 0:
                    audit_results.append(f"📁 File: {file_path}\n{result.stdout}\n" + "="*80)
                else:
                    audit_results.append(f"❌ Failed to audit {file_path}: {result.stderr or 'Unknown error'}")
                    
            except Exception as e:
                audit_results.append(f"❌ Error reading {file_path}: {str(e)}")
        
        return [TextContent(
            type="text",
            text=f"✅ Security audit completed!\n\nTarget: {target_path}\nAudited Files: {len(audit_results)}\nAudit Level: {audit_level}\n\n" + "\n\n".join(audit_results)
        )]
        
    except Exception as e:
        logger.exception("Security audit error")
        return [TextContent(type="text", text=f"❌ Security audit error: {str(e)}")]

async def performance_analysis_handler(args: Dict[str, Any]) -> List[TextContent]:
    file_path = args["file_path"]
    language = args["language"]
    
    try:
        if not os.path.exists(file_path):
            return [TextContent(type="text", text=f"❌ File not found: {file_path}")]
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        prompt = f"""Analyze this {language} code for performance bottlenecks and optimization opportunities.

Performance Analysis Areas:
- Algorithmic complexity (Big O analysis)
- Memory usage and optimization
- I/O operations efficiency
- Database query optimization
- Caching opportunities
- Resource management
- Concurrent/parallel processing potential
- Language-specific optimizations
- Scalability considerations
- Profiling recommendations

File: {file_path}
Language: {language}

Code:
```
{code_content}
```

Provide specific performance improvement recommendations with before/after examples where applicable."""
        
        result = run_gemini_command(["--prompt", prompt], timeout=90)
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=f"✅ Performance analysis completed!\n\nFile: {file_path}\nLanguage: {language}\n\nGemini Performance Analysis:\n{result.stdout}"
            )]
        else:
            return [TextContent(type="text", text=f"❌ Performance analysis failed: {result.stderr or 'Unknown error'}")]
            
    except Exception as e:
        logger.exception("Performance analysis error")
        return [TextContent(type="text", text=f"❌ Performance analysis error: {str(e)}")]

async def code_quality_report_handler(args: Dict[str, Any]) -> List[TextContent]:
    project_path = args["project_path"]
    include_metrics = args.get("include_metrics", True)
    
    try:
        if not os.path.exists(project_path):
            return [TextContent(type="text", text=f"❌ Project path not found: {project_path}")]
        
        # Analyze project structure
        structure_info = []
        file_count = 0
        for root, dirs, files in os.walk(project_path):
            # Skip common build/dependency directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv', 'build', 'dist']]
            
            level = root.replace(project_path, '').count(os.sep)
            indent = '  ' * level
            structure_info.append(f"{indent}{os.path.basename(root)}/")
            
            subindent = '  ' * (level + 1)
            for file in files[:10]:  # Limit files shown per directory
                structure_info.append(f"{subindent}{file}")
                file_count += 1
                
            if file_count > 100:  # Limit total structure size
                structure_info.append(f"{subindent}... (truncated)")
                break
        
        structure_summary = "\n".join(structure_info[:100])  # Limit output
        
        # Find key files for analysis
        key_files = []
        patterns = ["**/package.json", "**/requirements.txt", "**/pom.xml", "**/Cargo.toml", "**/go.mod", "**/*.md"]
        for pattern in patterns:
            key_files.extend(glob.glob(os.path.join(project_path, pattern), recursive=True))
        
        # Read key configuration files
        config_content = ""
        for file_path in key_files[:5]:  # Limit to first 5 key files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()[:2000]  # Limit content
                    config_content += f"\n\n{file_path}:\n{content}"
            except:
                pass
        
        prompt = f"""Analyze this project and provide a comprehensive code quality report.

Project Path: {project_path}
Include Metrics: {include_metrics}

Project Structure:
{structure_summary}

Key Configuration Files:
{config_content}

Please provide a comprehensive analysis covering:

1. **Architecture Assessment**
   - Project structure and organization
   - Design patterns usage
   - Separation of concerns
   - Modularity and maintainability

2. **Code Quality Metrics** (if include_metrics is True)
   - Estimated complexity
   - Maintainability index
   - Technical debt indicators
   - Documentation coverage

3. **Best Practices Compliance**
   - Language-specific conventions
   - Security practices
   - Performance considerations
   - Testing strategy

4. **Improvement Recommendations**
   - Priority issues to address
   - Refactoring opportunities
   - Infrastructure improvements
   - Development workflow enhancements

5. **Risk Assessment**
   - Security vulnerabilities
   - Performance bottlenecks
   - Maintenance challenges
   - Scalability concerns

Provide actionable recommendations with priority levels."""
        
        result = run_gemini_command(["--prompt", prompt], timeout=150)
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=f"✅ Code quality report generated!\n\nProject: {project_path}\nMetrics Included: {include_metrics}\n\nGemini Quality Report:\n{result.stdout}"
            )]
        else:
            return [TextContent(type="text", text=f"❌ Quality report generation failed: {result.stderr or 'Unknown error'}")]
            
    except Exception as e:
        logger.exception("Quality report error")
        return [TextContent(type="text", text=f"❌ Quality report error: {str(e)}")]

async def ask_gemini_handler(args: Dict[str, Any]) -> List[TextContent]:
    prompt = args["prompt"]
    include_all_files = args.get("include_all_files", False)
    
    try:
        # Build Gemini command arguments
        cmd_args = ["--prompt", prompt]
        if include_all_files:
            cmd_args.extend(["--all_files"])
        
        # Execute Gemini CLI using the robust wrapper
        result = run_gemini_command(cmd_args, timeout=120)
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=f"✅ Gemini Response:\n\n{result.stdout}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ Gemini Error:\n{result.stderr or 'Unknown error occurred'}"
            )]
            
    except subprocess.TimeoutExpired:
        return [TextContent(type="text", text="⏰ Gemini request timed out")]
    except FileNotFoundError as e:
        return [TextContent(type="text", text=f"❌ Gemini CLI not found: {str(e)}")]
    except Exception as e:
        logger.exception("Error in ask_gemini_handler")
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]

async def main():
    # Test Gemini CLI availability on startup
    try:
        logger.info("Testing Gemini CLI availability...")
        result = run_gemini_command(["--version"], timeout=10)
        if result.returncode == 0:
            logger.info(f"✅ Gemini CLI is available: {result.stdout.strip()}")
        else:
            logger.warning(f"⚠️ Gemini CLI test failed: {result.stderr}")
    except Exception as e:
        logger.error(f"❌ Gemini CLI test failed: {str(e)}")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, 
            write_stream, 
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
