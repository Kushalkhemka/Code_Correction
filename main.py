import os
import sys
import json
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.tool import FunctionTool

env_file = Path(__file__).parent / ".env"
load_dotenv(env_file, override=True)

api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    if api_key == "your-api-key-here":
        print("✗ Using placeholder API key - need to override system environment variable")
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    real_api_key = line.split('=', 1)[1].strip()
                    os.environ['OPENAI_API_KEY'] = real_api_key
                    api_key = real_api_key
                    print(f"✓ Loaded real API key from .env file: {api_key[:10]}...{api_key[-4:]} (length: {len(api_key)})")
                    break
    else:
        print(f"✓ API key loaded: {api_key[:10]}...{api_key[-4:]} (length: {len(api_key)})")
else:
    print("✗ API key not found in environment variables")
    print("Available environment variables:")
    for key in os.environ.keys():
        if 'openai' in key.lower() or 'api' in key.lower():
            print(f"  - {key}")

BASE_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PYTHON_PROGRAMS_DIR = BASE_DIR / "python_programs"
FIXED_PROGRAMS_DIR = BASE_DIR / "fixed_programs"
JSON_TESTCASES_DIR = BASE_DIR / "json_testcases"
PYTHON_TESTCASES_DIR = BASE_DIR / "python_testcases"

print(f"Current script path: {BASE_DIR}")
print(f"Python programs directory: {PYTHON_PROGRAMS_DIR}")
print(f"Fixed programs directory: {FIXED_PROGRAMS_DIR}")

if not FIXED_PROGRAMS_DIR.exists():
    FIXED_PROGRAMS_DIR.mkdir()
    with open(FIXED_PROGRAMS_DIR / "__init__.py", "w") as f:
        pass

available_programs = []
if PYTHON_PROGRAMS_DIR.exists():
    available_programs = [f.stem for f in PYTHON_PROGRAMS_DIR.glob("*.py") 
                         if f.name != "__init__.py" and not f.stem.endswith("_test")]
    print(f"Found {len(available_programs)} Python programs:")
    for program in available_programs[:5]:
        print(f"- {program}")
    if len(available_programs) > 5:
        print(f"... and {len(available_programs) - 5} more")
else:
    print(f"ERROR: Python programs directory not found at {PYTHON_PROGRAMS_DIR}")
    sys.exit(1)

async def read_code(context, arguments) -> str:
    """Read the source code of a Python program."""
    print(f"Debug - read_code called with context: {type(context)}, arguments: {arguments}")
    
    if isinstance(arguments, dict):
        program_name = arguments.get('program_name', '')
    elif isinstance(arguments, str):
        try:
            parsed_args = json.loads(arguments)
            program_name = parsed_args.get('program_name', '')
            print(f"Debug - extracted program_name from JSON: '{program_name}'")
        except json.JSONDecodeError:
            print("Debug - failed to parse JSON arguments")
            return "Error: Could not parse parameters"
    else:
        print(f"Debug - unexpected arguments type: {type(arguments)}")
        return "Error: Unexpected parameter format"
    
    if not program_name:
        return "Error: Missing program_name parameter"
    
    program_name = program_name.strip()
    
    file_path = PYTHON_PROGRAMS_DIR / f"{program_name}.py"
    print(f"Attempting to read file: {file_path}")
    
    if not file_path.exists():
        print("Files in python_programs directory:")
        for f in PYTHON_PROGRAMS_DIR.glob("*.py"):
            print(f"- {f.name}")
        return f"Error: Program '{program_name}' not found at {file_path}"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        
        print(f"Successfully read {len(code)} characters from {program_name}.py")
        return code
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return f"Error reading file: {str(e)}"

async def read_testcases(context, arguments) -> str:
    """Read the test cases for a Python program."""
    print(f"Debug - read_testcases called with context: {type(context)}, arguments: {arguments}")
    
    if isinstance(arguments, dict):
        program_name = arguments.get('program_name', '')
    elif isinstance(arguments, str):
        try:
            parsed_args = json.loads(arguments)
            program_name = parsed_args.get('program_name', '')
            print(f"Debug - extracted program_name from JSON for testcases: '{program_name}'")
        except json.JSONDecodeError:
            print("Debug - failed to parse JSON arguments for testcases")
            return "Error: Could not parse parameters"
    else:
        print(f"Debug - unexpected arguments type for testcases: {type(arguments)}")
        return "Error: Unexpected parameter format"
    
    if not program_name:
        return "Error: Missing program_name parameter"
    
    program_name = program_name.strip()
    
    graph_based = ["breadth_first_search", "depth_first_search", "detect_cycle",
                  "minimum_spanning_tree", "reverse_linked_list", "shortest_path_length",
                  "shortest_path_lengths", "shortest_paths", "topological_ordering"]
    
    if program_name in graph_based:
        file_path = PYTHON_TESTCASES_DIR / f"test_{program_name}.py"
        if not file_path.exists():
            return f"Error: Test file for {program_name} not found at {file_path}"
        
        with open(file_path, "r") as f:
            test_code = f.read()
        
        return f"Graph-based program test:\n{test_code}"
    else:
        file_path = JSON_TESTCASES_DIR / f"{program_name}.json"
        if not file_path.exists():
            return f"Error: Test cases for {program_name} not found at {file_path}"
        
        with open(file_path, "r") as f:
            test_cases = f.read()
        
        return test_cases

async def write_code(context, arguments) -> str:
    """Write fixed code to a file."""
    print(f"Debug - write_code called with context: {type(context)}, arguments: {arguments}")
    
    if isinstance(arguments, dict):
        program_name = arguments.get('program_name', '')
        fixed_code = arguments.get('fixed_code', '')
    elif isinstance(arguments, str):
        try:
            parsed_args = json.loads(arguments)
            program_name = parsed_args.get('program_name', '')
            fixed_code = parsed_args.get('fixed_code', '')
            print(f"Debug - extracted from JSON: program_name='{program_name}', fixed_code length={len(fixed_code)}")
        except json.JSONDecodeError:
            print("Debug - failed to parse JSON arguments for write")
            return "Error: Could not parse parameters"
    else:
        print(f"Debug - unexpected arguments type for write: {type(arguments)}")
        return "Error: Unexpected parameter format"
    
    if not program_name or not fixed_code:
        return f"Error: Missing required parameters. program_name='{program_name}', fixed_code length={len(fixed_code)}"
    
    program_name = program_name.strip()
    file_path = FIXED_PROGRAMS_DIR / f"{program_name}.py"
    
    try:
        with open(file_path, "w") as f:
            f.write(fixed_code)
        print(f"Successfully wrote {len(fixed_code)} characters to {file_path}")
        return f"Fixed code written to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

code_reader_tool = FunctionTool(
    name="read_code",
    description="Reads a Python file and returns its contents",
    params_json_schema={
        "type": "object",
        "properties": {
            "program_name": {"type": "string", "description": "Name of the program to read"}
        },
        "required": ["program_name"],
        "additionalProperties": False
    },
    on_invoke_tool=read_code
)

testcase_reader_tool = FunctionTool(
    name="read_testcases",
    description="Reads test cases for a Python program",
    params_json_schema={
        "type": "object",
        "properties": {
            "program_name": {"type": "string", "description": "Name of the program to read test cases for"}
        },
        "required": ["program_name"],
        "additionalProperties": False
    },
    on_invoke_tool=read_testcases
)

code_writer_tool = FunctionTool(
    name="write_code",
    description="Writes fixed code to a file",
    params_json_schema={
        "type": "object",
        "properties": {
            "program_name": {"type": "string", "description": "Name of the program to write"},
            "fixed_code": {"type": "string", "description": "Fixed code to write to file"}
        },
        "required": ["program_name", "fixed_code"],
        "additionalProperties": False
    },
    on_invoke_tool=write_code
)

bug_finder_agent = Agent(
    name="BugFinder",
    instructions="""
    You are a Bug Finder agent specialized in analyzing Python code.
    
    Your task is to:
    1. Read the provided Python code using the read_code tool
    2. Analyze it line by line to find a single bug
    3. Identify exactly which line contains the bug
    4. Explain what the bug is and why it's problematic
    5. Suggest a fix for the bug
    
    Return your analysis in JSON format with these fields:
    {
        "line_number": the line number where the bug appears,
        "buggy_line": the exact line of code with the bug,
        "bug_type": the type of bug (e.g., "off-by-one error", "incorrect operator"),
        "explanation": why this is a bug,
        "fix_suggestion": how to fix the bug
    }
    """,
    model="o3-mini",
    tools=[code_reader_tool, testcase_reader_tool]
)

bug_fixer_agent = Agent(
    name="BugFixer",
    instructions="""
    You are a Bug Fixer agent specialized in fixing Python code bugs.
    
    Your task is to:
    1. Read the provided Python code using the read_code tool
    2. Read the test cases to understand expected behavior using the read_testcases tool
    3. Fix the bug identified in the bug analysis
    4. Write the fixed code using the write_code tool
    
    Return your fixed code and explanation in this format:
    
    BUG FIX:
    - Original Bug: <brief description of the bug>
    - Fix Applied: <description of your fix>
    - Reasoning: <explain why your fix resolves the issue>
    """,
    model="o3-mini",
    tools=[code_reader_tool, testcase_reader_tool, code_writer_tool]
)

async def analyze_and_fix_program(program_name):
    if program_name not in available_programs:
        print(f"ERROR: Program '{program_name}' not found. Available programs:")
        for prog in available_programs[:10]:
            print(f"- {prog}")
        return
    
    print(f"\n=== Analyzing program: {program_name} ===")
    
    file_path = PYTHON_PROGRAMS_DIR / f"{program_name}.py"
    if not file_path.exists():
        print(f"ERROR: Program file '{file_path}' does not exist")
        return
    else:
        print(f"Confirmed program file exists: {file_path}")
        
    print(f"Running bug finder agent on {program_name}...")
    bug_result = await Runner.run(
        bug_finder_agent, 
        f"Use the read_code tool to read the source code of '{program_name}', then analyze it to find the bug."
    )
    bug_analysis = bug_result.final_output
    print(f"\nBug Analysis Result:")
    print(bug_analysis)
    
    print(f"\nRunning bug fixer agent on {program_name}...")
    fix_result = await Runner.run(
        bug_fixer_agent, 
        f"Use the read_code tool to read the source code of '{program_name}', then fix it based on this analysis: {bug_analysis}"
    )
    fix_result_output = fix_result.final_output
    print(f"\nFix Result:")
    print(fix_result_output)
    
    return {
        "program": program_name,
        "bug_analysis": bug_analysis,
        "fix_result": fix_result_output
    }

if __name__ == "__main__":
    program_name = sys.argv[1] if len(sys.argv) > 1 else "gcd"
    
    print(f"Starting analysis of program: {program_name}")
    try:
        print(f"Checking program file...")
        test_file = PYTHON_PROGRAMS_DIR / f"{program_name}.py"
        if test_file.exists():
            with open(test_file, "r") as f:
                content = f.read()
                print(f"File content verification: {len(content)} characters")
        else:
            print(f"WARNING: File {test_file} does not exist")
        
        print("Creating event loop...")
        loop = asyncio.get_event_loop()
        print(f"Running async analysis for {program_name}...")
        result = loop.run_until_complete(analyze_and_fix_program(program_name))
        print("Analysis completed")
    except KeyboardInterrupt:
        print("Operation cancelled by user")
    except Exception as e:
        print(f"Error running analysis: {str(e)}")
        import traceback
        traceback.print_exc()