import os
import sys
import json
import asyncio
import time
from pathlib import Path
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.tool import FunctionTool
from datetime import datetime
import logging
from openai import AsyncOpenAI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deepseek_analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

env_file = Path(__file__).parent / ".env"
load_dotenv(env_file, override=True)

DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')

if not deepseek_api_key:
    logger.error("DEEPSEEK_API_KEY not found in environment variables")
    sys.exit(1)

logger.info(f"DeepSeek API key loaded: {deepseek_api_key[:15]}...{deepseek_api_key[-4:]} (length: {len(deepseek_api_key)})")

BASE_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
PYTHON_PROGRAMS_DIR = BASE_DIR / "python_programs"
FIXED_PROGRAMS_DIR = BASE_DIR / "fixed_programs_deepseek"
JSON_TESTCASES_DIR = BASE_DIR / "json_testcases"
PYTHON_TESTCASES_DIR = BASE_DIR / "python_testcases"
RESULTS_DIR = BASE_DIR / "deepseek_results"

for dir_path in [FIXED_PROGRAMS_DIR, RESULTS_DIR]:
    if not dir_path.exists():
        dir_path.mkdir()
        if dir_path == FIXED_PROGRAMS_DIR:
            with open(dir_path / "__init__.py", "w") as f:
                pass

available_programs = []
if PYTHON_PROGRAMS_DIR.exists():
    available_programs = [f.stem for f in PYTHON_PROGRAMS_DIR.glob("*.py") 
                         if f.name != "__init__.py" and not f.stem.endswith("_test")]
    logger.info(f"Found {len(available_programs)} programs to analyze with DeepSeek")

BUG_CATEGORIES = [
    "Incorrect assignment operator",
    "Incorrect variable", 
    "Incorrect comparison operator",
    "Missing condition",
    "Missing/added +1",
    "Variable swap",
    "Incorrect array slice",
    "Variable prepend",
    "Incorrect data structure constant",
    "Incorrect method called",
    "Incorrect field dereference",
    "Missing arithmetic expression",
    "Missing function call",
    "Missing line"
]

async def read_code(context, arguments) -> str:
    if isinstance(arguments, dict):
        program_name = arguments.get('program_name', '')
    elif isinstance(arguments, str):
        try:
            parsed_args = json.loads(arguments)
            program_name = parsed_args.get('program_name', '')
        except json.JSONDecodeError:
            return "Error: Could not parse parameters"
    
    if not program_name:
        return "Error: Missing program_name parameter"
    
    program_name = program_name.strip()
    file_path = PYTHON_PROGRAMS_DIR / f"{program_name}.py"
    
    if not file_path.exists():
        return f"Error: Program '{program_name}' not found"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        return code
    except Exception as e:
        return f"Error reading file: {str(e)}"

async def read_testcases(context, arguments) -> str:
    if isinstance(arguments, dict):
        program_name = arguments.get('program_name', '')
    elif isinstance(arguments, str):
        try:
            parsed_args = json.loads(arguments)
            program_name = parsed_args.get('program_name', '')
        except json.JSONDecodeError:
            return "Error: Could not parse parameters"
    
    if not program_name:
        return "Error: Missing program_name parameter"
    
    program_name = program_name.strip()
    
    graph_based = ["breadth_first_search", "depth_first_search", "detect_cycle",
                  "minimum_spanning_tree", "reverse_linked_list", "shortest_path_length",
                  "shortest_path_lengths", "shortest_paths", "topological_ordering"]
    
    if program_name in graph_based:
        file_path = PYTHON_TESTCASES_DIR / f"test_{program_name}.py"
        if not file_path.exists():
            return f"Error: Test file for {program_name} not found"
        
        with open(file_path, "r") as f:
            test_code = f.read()
        
        return f"Graph-based program test:\n{test_code}"
    else:
        file_path = JSON_TESTCASES_DIR / f"{program_name}.json"
        if not file_path.exists():
            return f"Error: Test cases for {program_name} not found"
        
        with open(file_path, "r") as f:
            test_cases = f.read()
        
        return test_cases

async def write_code_with_classification(context, arguments) -> str:
    if isinstance(arguments, dict):
        program_name = arguments.get('program_name', '')
        fixed_code = arguments.get('fixed_code', '')
        bug_classification = arguments.get('bug_classification', 'Unknown')
        bug_description = arguments.get('bug_description', '')
    elif isinstance(arguments, str):
        try:
            parsed_args = json.loads(arguments)
            program_name = parsed_args.get('program_name', '')
            fixed_code = parsed_args.get('fixed_code', '')
            bug_classification = parsed_args.get('bug_classification', 'Unknown')
            bug_description = parsed_args.get('bug_description', '')
        except json.JSONDecodeError:
            return "Error: Could not parse parameters"
    
    if not program_name or not fixed_code:
        return f"Error: Missing required parameters"
    
    program_name = program_name.strip()
    file_path = FIXED_PROGRAMS_DIR / f"{program_name}.py"
    
    header_comment = f"""# Fixed Program: {program_name} (DeepSeek)
# Bug Classification: {bug_classification}
# Bug Description: {bug_description}
# Fixed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# LLM Used: DeepSeek
# 
# Original bug was classified as: {bug_classification}
# This indicates: {bug_description}

"""
    
    final_code = header_comment + fixed_code
    
    try:
        with open(file_path, "w") as f:
            f.write(final_code)
        return f"Fixed code with classification written to {file_path}"
    except Exception as e:        return f"Error writing file: {str(e)}"

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
    name="write_code_with_classification",
    description="Writes fixed code to a file with bug classification header",
    params_json_schema={
        "type": "object",
        "properties": {
            "program_name": {"type": "string", "description": "Name of the program to write"},
            "fixed_code": {"type": "string", "description": "Fixed code to write to file"},
            "bug_classification": {"type": "string", "description": "Bug category classification"},
            "bug_description": {"type": "string", "description": "Description of the bug"}
        },
        "required": ["program_name", "fixed_code", "bug_classification", "bug_description"],
        "additionalProperties": False
    },
    on_invoke_tool=write_code_with_classification
)

deepseek_client = AsyncOpenAI(base_url=DEEPSEEK_BASE_URL, api_key=deepseek_api_key)
deepseek_model = OpenAIChatCompletionsModel(model="deepseek-chat", openai_client=deepseek_client)

bug_finder_agent = Agent(
    name="DeepSeekBugClassifier",
    instructions=f"""
    You are DeepSeek, a Bug Classifier agent specialized in analyzing Python code and classifying bugs.
    
    Your task is to:
    1. Read the provided Python code using the read_code tool
    2. Analyze it line by line to find a single bug
    3. Identify exactly which line contains the bug
    4. Classify the bug into one of these specific categories:
    
    BUG CATEGORIES:
    {chr(10).join(f"- {category}" for category in BUG_CATEGORIES)}
    
    5. Explain what the bug is and why it's problematic
    6. Suggest a fix for the bug
    
    Return your analysis in JSON format with these fields:
    {{
        "line_number": the line number where the bug appears,
        "buggy_line": the exact line of code with the bug,
        "bug_type": one of the exact categories listed above,
        "explanation": why this is a bug and how it fits the category,
        "fix_suggestion": how to fix the bug
    }}
    
    IMPORTANT: The bug_type must be exactly one of the categories listed above.
    """,
    model=deepseek_model,
    tools=[code_reader_tool, testcase_reader_tool]
)

bug_fixer_agent = Agent(
    name="DeepSeekBugFixer",
    instructions=f"""
    You are DeepSeek, a Bug Fixer agent specialized in fixing Python code bugs with proper classification.
    
    Your task is to:
    1. Read the provided Python code using the read_code tool
    2. Read the test cases to understand expected behavior using the read_testcases tool
    3. Fix the bug identified in the bug analysis
    4. Write the fixed code using the write_code_with_classification tool with proper classification
    
    When writing the fixed code, you must:
    - Extract the bug_type from the bug analysis
    - Ensure the bug_type is one of these exact categories:
    {chr(10).join(f"  - {category}" for category in BUG_CATEGORIES)}
    - Provide a clear description of what the bug was
    - Write the complete fixed code
    
    Return your response in this format:
    
    BUG FIX COMPLETE (DeepSeek):
    - Bug Classification: [exact category from the list above]
    - Original Bug: [brief description of the bug]
    - Fix Applied: [description of your fix]
    - Reasoning: [explain why your fix resolves the issue]
    
    The fixed code has been written to the file with proper classification header.
    """,
    model=deepseek_model,
    tools=[code_reader_tool, testcase_reader_tool, code_writer_tool]
)

async def analyze_single_program(program_name: str) -> dict:
    start_time = time.time()
    
    try:
        bug_result = await Runner.run(
            bug_finder_agent, 
            f"Use the read_code tool to read the source code of '{program_name}', then analyze it to find and classify the bug into one of the specific bug categories."
        )
        bug_analysis = bug_result.final_output
        
        # Step 2: Fix the bug with classification
        fix_result = await Runner.run(
            bug_fixer_agent, 
            f"Use the read_code tool to read the source code of '{program_name}', then fix it based on this analysis: {bug_analysis}. Make sure to use the write_code_with_classification tool to save the fixed code with proper bug classification."
        )
        fix_result_output = fix_result.final_output
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Extract bug classification from analysis
        bug_classification = "Unknown"
        try:
            if "bug_type" in bug_analysis:
                import re
                bug_type_match = re.search(r'"bug_type":\s*"([^"]+)"', bug_analysis)
                if bug_type_match:
                    bug_classification = bug_type_match.group(1)
        except:
            pass
        
        result = {
            "program": program_name,
            "status": "success",
            "duration_seconds": round(duration, 2),
            "bug_classification": bug_classification,
            "bug_analysis": bug_analysis,
            "fix_result": fix_result_output,
            "llm_used": "DeepSeek",
            "timestamp": datetime.now().isoformat()
        }
        
        # Save individual result
        result_file = RESULTS_DIR / f"{program_name}_result.json"
        with open(result_file, "w") as f:
            json.dump(result, f, indent=2)
        
        logger.info(f"✓ {program_name} completed in {duration:.2f}s - Bug: {bug_classification}")
        return result
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        
        result = {
            "program": program_name,
            "status": "error",
            "duration_seconds": round(duration, 2),
            "error": str(e),
            "llm_used": "DeepSeek",
            "timestamp": datetime.now().isoformat()
        }
        
        result_file = RESULTS_DIR / f"{program_name}_result.json"
        with open(result_file, "w") as f:
            json.dump(result, f, indent=2)
        
        logger.error(f"✗ {program_name} failed in {duration:.2f}s: {str(e)}")
        return result

async def run_batch_analysis(programs_to_analyze=None):
    """Run analysis on multiple programs with DeepSeek."""
    if programs_to_analyze is None:
        programs_to_analyze = available_programs
    
    logger.info(f"Starting DeepSeek batch analysis of {len(programs_to_analyze)} programs")
    
    start_time = time.time()
    
    # Create tasks for all programs
    tasks = [analyze_single_program(program) for program in programs_to_analyze]
    
    # Execute all tasks in parallel
    results = []
    completed = 0
    total = len(tasks)
    
    for coro in asyncio.as_completed(tasks):
        result = await coro
        completed += 1
        results.append(result)
        
        progress = (completed / total) * 100
        bug_info = f" - {result.get('bug_classification', 'Unknown')}" if result['status'] == 'success' else ""
        print(f"DeepSeek Progress: {completed}/{total} ({progress:.1f}%) - {result['program']} ({result['status']}){bug_info}")
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Generate summary
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "error"]
    
    # Bug classification statistics
    bug_stats = {}
    for result in successful:
        bug_type = result.get('bug_classification', 'Unknown')
        bug_stats[bug_type] = bug_stats.get(bug_type, 0) + 1
    
    summary = {
        "llm_used": "DeepSeek",
        "total_programs": total,
        "successful": len(successful),
        "failed": len(failed),
        "total_duration_seconds": round(total_duration, 2),
        "average_duration_seconds": round(total_duration / total, 2),
        "programs_per_minute": round((total / total_duration) * 60, 2),
        "bug_classification_statistics": bug_stats,
        "timestamp": datetime.now().isoformat(),
        "successful_programs": [{"program": r["program"], "bug_type": r.get("bug_classification", "Unknown")} for r in successful],
        "failed_programs": [{"program": r["program"], "error": r["error"]} for r in failed],
        "results": results
    }
    
    # Save summary
    summary_file = RESULTS_DIR / f"deepseek_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print final summary
    print(f"\n{'='*60}")
    print(f"DEEPSEEK ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"Total Programs: {total}")
    print(f"Successful: {len(successful)} ({len(successful)/total*100:.1f}%)")
    print(f"Failed: {len(failed)} ({len(failed)/total*100:.1f}%)")
    print(f"Total Duration: {total_duration:.2f} seconds")
    print(f"Average per Program: {total_duration/total:.2f} seconds")
    print(f"Processing Rate: {(total/total_duration)*60:.1f} programs/minute")
    
    if bug_stats:
        print(f"\nBUG CLASSIFICATION STATISTICS:")
        print(f"{'='*40}")
        for bug_type, count in sorted(bug_stats.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(successful)) * 100
            print(f"{bug_type}: {count} ({percentage:.1f}%)")
    
    print(f"\nResults saved to: {RESULTS_DIR}")
    print(f"Fixed programs saved to: {FIXED_PROGRAMS_DIR}")
    
    return summary

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            programs_to_run = available_programs
        else:
            programs_to_run = sys.argv[1:]
            invalid_programs = [p for p in programs_to_run if p not in available_programs]
            if invalid_programs:
                logger.error(f"Invalid programs: {invalid_programs}")
                sys.exit(1)
    else:
        programs_to_run = available_programs[:5]
        logger.info(f"No arguments provided. Running first 5 programs: {programs_to_run}")
    
    logger.info(f"Selected programs for DeepSeek analysis: {len(programs_to_run)} total")
    
    try:
        asyncio.run(run_batch_analysis(programs_to_run))
    except KeyboardInterrupt:
        logger.info("DeepSeek analysis interrupted by user")
    except Exception as e:
        logger.error(f"DeepSeek analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()