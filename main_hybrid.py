import os
import sys
import json
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.tool import FunctionTool
from test_runner_native import NativeTestRunner

env_file = Path(__file__).parent / ".env"
load_dotenv(env_file, override=True)

api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    if api_key == "your-api-key-here":
        print("Using placeholder API key - need to override system environment variable")
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    real_api_key = line.split('=', 1)[1].strip()
                    os.environ['OPENAI_API_KEY'] = real_api_key
                    api_key = real_api_key
                    print(f"Loaded real API key from .env file: {api_key[:10]}...{api_key[-4:]} (length: {len(api_key)})")
                    break
    else:
        print(f"API key loaded: {api_key[:10]}...{api_key[-4:]} (length: {len(api_key)})")
else:    print("API key not found in environment variables")

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
    with open(FIXED_PROGRAMS_DIR / "__init__.py", "w") as f:        pass

test_runner = NativeTestRunner(BASE_DIR)

# List all available programs
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

# Simple function tools (from main.py)
async def read_code(context, arguments) -> str:
    """Read the source code of a Python program."""
    if isinstance(arguments, dict):
        program_name = arguments.get('program_name', '')
    elif isinstance(arguments, str):
        try:
            parsed_args = json.loads(arguments)
            program_name = parsed_args.get('program_name', '')
        except json.JSONDecodeError:
            return "Error: Could not parse parameters"
    else:
        return "Error: Unexpected parameter format"
    
    if not program_name:
        return "Error: Missing program_name parameter"
    
    program_name = program_name.strip()
    file_path = PYTHON_PROGRAMS_DIR / f"{program_name}.py"
    
    if not file_path.exists():
        return f"Error: Program '{program_name}' not found at {file_path}"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        return code
    except Exception as e:
        return f"Error reading file: {str(e)}"

async def read_testcases(context, arguments) -> str:
    """Read the test cases for a Python program."""
    if isinstance(arguments, dict):
        program_name = arguments.get('program_name', '')
    elif isinstance(arguments, str):
        try:
            parsed_args = json.loads(arguments)
            program_name = parsed_args.get('program_name', '')
        except json.JSONDecodeError:
            return "Error: Could not parse parameters"
    else:
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
    if isinstance(arguments, dict):
        program_name = arguments.get('program_name', '')
        fixed_code = arguments.get('fixed_code', '')
    elif isinstance(arguments, str):
        try:
            parsed_args = json.loads(arguments)
            program_name = parsed_args.get('program_name', '')
            fixed_code = parsed_args.get('fixed_code', '')
        except json.JSONDecodeError:
            return "Error: Could not parse parameters"
    else:
        return "Error: Unexpected parameter format"
    
    if not program_name or not fixed_code:
        return f"Error: Missing required parameters"
    
    program_name = program_name.strip()
    file_path = FIXED_PROGRAMS_DIR / f"{program_name}.py"
    
    try:
        with open(file_path, "w") as f:
            f.write(fixed_code)
        return f"Fixed code written to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# Simple test function
async def test_code_simple(context, arguments) -> str:
    """Test code using NativeTestRunner - simple version."""
    if isinstance(arguments, dict):
        program_name = arguments.get('program_name', '')
        mode = arguments.get('mode', 'fixed')
    elif isinstance(arguments, str):
        try:
            parsed_args = json.loads(arguments)
            program_name = parsed_args.get('program_name', '')
            mode = parsed_args.get('mode', 'fixed')
        except json.JSONDecodeError:
            return "Error: Could not parse parameters"
    else:
        return "Error: Unexpected parameter format"
    
    if not program_name:
        return "Error: Missing program_name parameter"
    
    program_name = program_name.strip()
    
    try:
        result = test_runner.run_test(program_name, mode)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error running tests: {str(e)}"

# Enhanced test function with verbose output (for advanced mode)
async def test_code_verbose(context, arguments) -> str:
    """Test code using NativeTestRunner with detailed verbose output."""
    if isinstance(arguments, dict):
        program_name = arguments.get('program_name', '')
        mode = arguments.get('mode', 'fixed')
        compare_versions = arguments.get('compare_versions', False)
        show_details = arguments.get('show_details', True)
    elif isinstance(arguments, str):
        try:
            parsed_args = json.loads(arguments)
            program_name = parsed_args.get('program_name', '')
            mode = parsed_args.get('mode', 'fixed')
            compare_versions = parsed_args.get('compare_versions', False)
            show_details = parsed_args.get('show_details', True)
        except json.JSONDecodeError:
            return "Error: Could not parse parameters"
    else:
        return "Error: Unexpected parameter format"
    
    if not program_name:
        return "Error: Missing program_name parameter"
    
    program_name = program_name.strip()
    
    try:
        result = test_runner.run_test(program_name, mode)
        
        # Add detailed failure analysis if requested
        if show_details and result.get("failed_tests"):
            json_file = BASE_DIR / "json_testcases" / f"{program_name}.json"
            if json_file.exists():
                with open(json_file, 'r') as f:
                    test_cases = []
                    for line in f:
                        line = line.strip()
                        if line:
                            test_cases.append(json.loads(line))
                
                enhanced_failures = []
                for i, failure in enumerate(result["failed_tests"]):
                    if i < len(test_cases):
                        inputs, expected = test_cases[i]
                        enhanced_failures.append({
                            "test_number": i + 1,
                            "input": inputs,
                            "expected": expected,
                            "failure_description": failure
                        })
                    else:
                        enhanced_failures.append({
                            "failure_description": failure
                        })
                
                result["detailed_failures"] = enhanced_failures
        
        if compare_versions:
            buggy_result = test_runner.run_test(program_name, "buggy")
            correct_result = test_runner.run_test(program_name, "correct")
            
            comparison_results = {
                "fixed": result,
                "buggy": buggy_result,
                "correct": correct_result,
                "comparison_analysis": {
                    "fixed_vs_buggy": f"Fixed: {result['pass_rate']:.1%}, Buggy: {buggy_result['pass_rate']:.1%}",
                    "fixed_vs_correct": f"Fixed: {result['pass_rate']:.1%}, Correct: {correct_result['pass_rate']:.1%}",
                    "improvement": result['passed'] - buggy_result['passed']
                }
            }
            return json.dumps(comparison_results, indent=2)
        else:
            return json.dumps(result, indent=2)
            
    except Exception as e:
        return f"Error running tests: {str(e)}"

# Create tools
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

# Simple test tool
simple_test_tool = FunctionTool(
    name="test_code",
    description="Tests code using NativeTestRunner",
    params_json_schema={
        "type": "object",
        "properties": {
            "program_name": {"type": "string", "description": "Name of the program to test"},
            "mode": {"type": "string", "description": "Test mode: buggy, correct, or fixed", "enum": ["buggy", "correct", "fixed"]}
        },
        "required": ["program_name", "mode"],
        "additionalProperties": False
    },
    on_invoke_tool=test_code_simple
)

# Verbose test tool
verbose_test_tool = FunctionTool(
    name="test_code_verbose",
    description="Tests code using NativeTestRunner with detailed verbose output",
    params_json_schema={
        "type": "object",
        "properties": {
            "program_name": {"type": "string", "description": "Name of the program to test"},
            "mode": {"type": "string", "description": "Test mode: buggy, correct, or fixed", "enum": ["buggy", "correct", "fixed"]},
            "compare_versions": {"type": "boolean", "description": "Whether to compare with other versions"},
            "show_details": {"type": "boolean", "description": "Whether to show detailed failure analysis"}
        },
        "required": ["program_name", "mode", "compare_versions", "show_details"],
        "additionalProperties": False
    },
    on_invoke_tool=test_code_verbose
)

# SIMPLE AGENTS (like main.py)
simple_bug_finder = Agent(
    name="BugFinder",
    instructions="""
    You are a Bug Finder agent specialized in analyzing Python code.
    
    Your task is to:
    1. Read the provided Python code using the read_code tool
    2. Read the test cases using read_testcases tool to understand expected behavior
    3. Analyze it line by line to find bugs
    4. Identify exactly which line contains the bug
    5. Explain what the bug is and why it's problematic
    6. Suggest a fix for the bug
    
    Return your analysis in JSON format with these fields:
    {
        "line_number": the line number where the bug appears,
        "buggy_line": "the exact line of code with the bug",
        "bug_type": "the type of bug (e.g., off-by-one error, incorrect operator)",
        "explanation": "why this is a bug",
        "fix_suggestion": "how to fix the bug"
    }
    """,
    model="o3-mini",
    tools=[code_reader_tool, testcase_reader_tool]
)

simple_bug_fixer = Agent(
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

simple_evaluator = Agent(
    name="SimpleEvaluator",
    instructions="""
    You are a simple test evaluator that validates fixed code.
    
    Your task is to:
    1. Use test_code tool to test the fixed version with mode="fixed"
    2. Check if all tests pass
    3. Return a simple pass/fail result
    
    Return evaluation in JSON format:
    {
        "validation_passed": boolean,
        "pass_rate": float,
        "total_tests": int,
        "passed_tests": int,
        "summary": "brief summary of results"
    }
    """,
    model="o3-mini",
    tools=[simple_test_tool]
)

# ADVANCED AGENTS (like main_enhanced_cot.py)
advanced_bug_analyzer = Agent(
    name="AdvancedBugAnalyzer",
    instructions="""
    You are an expert Python debugging agent that uses Chain of Thought reasoning to identify bugs.
    
    TASK: Analyze Python code systematically to find bugs using deep reasoning.
    
    METHODOLOGY - Chain of Thought Analysis:
    
    1. ALGORITHM UNDERSTANDING:
       - First, read the code and test cases
       - Identify what algorithm this implements
       - Explain the expected behavior step by step
       - Map each line of code to its algorithmic purpose
    
    2. TRACE EXECUTION:
       - Pick 2-3 simple test cases
       - Manually trace through the code execution
       - Track all variable values at each step
       - Note where the actual behavior differs from expected
    
    3. BUG IDENTIFICATION:
       - Compare traced execution with expected algorithm
       - Identify logical errors, not just syntax errors
       - Consider edge cases and boundary conditions
       - Look for algorithmic mistakes, not just implementation bugs
    
    4. ROOT CAUSE ANALYSIS:
       - Explain WHY the bug occurs
       - What fundamental misunderstanding led to this bug
       - How does this affect the overall algorithm correctness
    
    Return your analysis in this detailed format:
    ```json
    {
        "algorithm_purpose": "Detailed explanation of what this algorithm should do",
        "code_walkthrough": "Step-by-step explanation of what the current code does",
        "execution_trace": {
            "test_case": "Simple test case you traced",
            "step_by_step": ["Step 1: ...", "Step 2: ...", "..."],
            "expected_result": "What should happen",
            "actual_result": "What actually happens"
        },
        "bug_analysis": {
            "line_numbers": [list of problematic lines],
            "bug_type": "Type of logical error",
            "root_cause": "Fundamental reason why this is wrong",
            "algorithmic_impact": "How this affects the algorithm's correctness"
        },
        "fix_strategy": "High-level approach to fix this bug"
    }
    ```
    
    Think step by step and be thorough in your analysis.
    """,
    model="o3-mini",
    tools=[code_reader_tool, testcase_reader_tool]
)

advanced_bug_fixer = Agent(
    name="AdvancedCodeFixer",
    instructions="""
    You are an expert code fixer that uses Self-Refine methodology to create correct solutions.
    
    TASK: Fix Python code bugs using systematic refinement and validation.
    
    METHODOLOGY - Self-Refine Approach:
    
    1. UNDERSTAND THE PROBLEM:
       - Read the bug analysis carefully
       - Understand the root cause, not just symptoms
       - Read test cases to understand expected behavior
       - If previous iterations failed, understand WHY they failed
    
    2. DESIGN THE SOLUTION:
       - Plan your fix based on algorithmic understanding
       - Don't just patch symptoms - fix the root cause
       - Consider multiple approaches and choose the best
       - Think about edge cases your fix should handle
    
    3. IMPLEMENT THE FIX:
       - Make precise changes to fix the algorithmic issue
       - Preserve the original algorithm structure when possible
       - Add comments explaining your changes
       - Ensure your fix is complete and robust
    
    4. SELF-VALIDATE:
       - Trace through your fixed code with test cases
       - Verify it handles edge cases correctly
       - Check that you haven't introduced new bugs
       - Ensure the fix addresses the root cause
    
    When you receive test failure feedback:
    - The feedback shows SPECIFIC test cases that failed
    - These failures indicate your previous fix was insufficient
    - You need to find a DIFFERENT bug or make a MORE COMPREHENSIVE fix
    - Don't just add safety checks - fix the underlying logic
    
    Return your response in this format:
    
    PROBLEM ANALYSIS:
    - Root cause understanding: [your analysis]
    - Previous iteration failures: [what went wrong before, if applicable]
    
    SOLUTION DESIGN:
    - Algorithmic approach: [how you plan to fix this]
    - Why this differs from previous attempts: [if applicable]
    
    IMPLEMENTATION:
    [Write the complete fixed code using write_code tool]
    
    VALIDATION:
    - Manual trace verification: [trace through one test case]
    - Edge cases handled: [list edge cases your fix addresses]
    """,
    model="o3-mini",
    tools=[code_reader_tool, testcase_reader_tool, code_writer_tool]
)

advanced_evaluator = Agent(
    name="AdvancedTestValidator",
    instructions="""
    You are an expert test evaluator that uses ReAct (Reasoning and Acting) methodology.
    
    TASK: Validate fixed code and provide actionable feedback using detailed test analysis.
    
    METHODOLOGY - ReAct Approach:
    
    1. OBSERVE (Test Execution):
       - Run comprehensive tests with detailed output
       - Compare fixed version with buggy and correct versions
       - Collect specific failure information
    
    2. REASON (Failure Analysis):
       - Analyze WHY specific tests failed
       - Look for patterns in the failures
       - Understand what the failures reveal about remaining bugs
       - Consider if this is a new bug or the same bug manifesting differently
    
    3. ACT (Provide Feedback):
       - Give specific, actionable recommendations
       - Identify the exact nature of remaining issues
       - Suggest concrete next steps for fixing
    
    CRITICAL ANALYSIS POINTS:
    - Look at the SPECIFIC test cases that failed
    - Compare input/expected/actual values
    - Identify if it's an off-by-one error, logic error, edge case issue, etc.
    - Determine if the algorithm approach itself is wrong
    
    When tests fail:
    - Don't just say "review the logic" - be SPECIFIC
    - Point to exact test cases and what they reveal
    - Suggest specific algorithmic changes needed
    - Identify if the current approach can be fixed or needs to be replaced
    
    Use test_code_verbose tool with mode="fixed", compare_versions=true, show_details=true
    
    Return evaluation in JSON format:
    {
        "validation_passed": boolean,
        "pass_rate": float,
        "total_tests": int,
        "passed_tests": int,
        "test_type": "JSON or Graph",
        "failure_analysis": {
            "failed_test_cases": [
                {
                    "test_number": int,
                    "input": "actual input values",
                    "expected": "expected output", 
                    "actual": "actual output",
                    "analysis": "specific reason why this failed"
                }
            ],
            "failure_patterns": "common patterns in failures",
            "bug_type": "type of bug causing failures"
        },
        "algorithmic_assessment": {
            "current_approach_viability": "can current approach work or needs replacement",
            "specific_issues": ["list of specific algorithmic issues"],
            "recommended_changes": ["specific changes needed"]
        },
        "actionable_recommendations": [
            "specific step 1",
            "specific step 2",
            "..."
        ]
    }
    """,
    model="o3-mini",
    tools=[verbose_test_tool]
)

# HYBRID MAIN FUNCTION
async def analyze_and_fix_program_hybrid(program_name, max_iterations=5):
    if program_name not in available_programs:
        print(f"ERROR: Program '{program_name}' not found. Available programs:")
        for prog in available_programs[:10]:
            print(f"- {prog}")
        return
    
    print(f"\n=== Hybrid Analysis of program: {program_name} ===")
    
    # Check file exists
    file_path = PYTHON_PROGRAMS_DIR / f"{program_name}.py"
    if not file_path.exists():
        print(f"ERROR: Program file '{file_path}' does not exist")
        return
    else:
        print(f"Confirmed program file exists: {file_path}")
    
    # PHASE 1: Simple approach (like main.py)
    print(f"\n--- PHASE 1: Simple Analysis (Fast Track) ---")
    
    # Step 1: Simple bug finding
    print(f"Running simple bug finder...")
    bug_result = await Runner.run(
        simple_bug_finder, 
        f"Use the read_code tool to read the source code of '{program_name}' and read_testcases to understand expected behavior, then analyze it to find the bug."
    )
    bug_analysis = bug_result.final_output
    print(f"Bug Analysis Result:")
    print(bug_analysis)
    
    # Step 2: Simple bug fixing
    print(f"Running simple bug fixer...")
    fix_result = await Runner.run(
        simple_bug_fixer, 
        f"Use the read_code tool to read the source code of '{program_name}', then fix it based on this analysis: {bug_analysis}"
    )
    fix_result_output = fix_result.final_output
    print(f"Fix Result:")
    print(fix_result_output)
    
    # Step 3: Simple evaluation
    print(f"Running simple evaluation...")
    eval_result = await Runner.run(
        simple_evaluator,
        f"Use the test_code tool to test the fixed version of '{program_name}' and provide simple evaluation."
    )
    eval_output = eval_result.final_output
    print(f"Simple Evaluation:")
    print(eval_output)
    
    # Check if simple approach worked
    try:
        eval_data = json.loads(eval_output)
        if eval_data.get("validation_passed", False):
            print(f"\nSUCCESS: Simple approach worked! All tests passed.")
            return {
                "program": program_name,
                "success": True,
                "approach": "simple",
                "iterations": 1,
                "bug_analysis": bug_analysis,
                "fix_result": fix_result_output,
                "test_evaluation": eval_output
            }
        else:
            pass_rate = eval_data.get("pass_rate", 0.0)
            print(f"\nSimple approach failed with {pass_rate:.1%} pass rate. Escalating to advanced mode...")
    except json.JSONDecodeError:
        print(f"\nSimple approach evaluation unclear. Escalating to advanced mode...")
    
    # PHASE 2: Advanced approach (like main_enhanced_cot.py)
    print(f"\n--- PHASE 2: Advanced Analysis (Deep Dive) ---")
    
    # Step 1: Deep bug analysis
    print(f"Running advanced bug analysis with Chain of Thought...")
    advanced_bug_result = await Runner.run(
        advanced_bug_analyzer, 
        f"Perform a deep Chain of Thought analysis of the '{program_name}' program. The simple approach failed, so we need deeper analysis. Read the code, understand the algorithm, trace execution, and identify the root cause of any bugs."
    )
    advanced_bug_analysis = advanced_bug_result.final_output
    print(f"Advanced Bug Analysis:")
    print(advanced_bug_analysis)
    
    # Iterative advanced fixing
    iteration = 1
    previous_failures = []
    test_feedback = ""
    
    while iteration <= max_iterations:
        print(f"\n--- Advanced Iteration {iteration}/{max_iterations} ---")
        
        # Step 2: Advanced fixing with Self-Refine
        print(f"Running advanced Self-Refine bug fixing...")
        advanced_fix_prompt = f"""
        Use Self-Refine methodology to fix the '{program_name}' program.
        
        Simple approach failed - we need a more sophisticated fix.
        
        Advanced Bug Analysis: {advanced_bug_analysis}
        
        Current Iteration: {iteration}/{max_iterations}
        """
        
        if iteration > 1:
            advanced_fix_prompt += f"""
        
        CRITICAL: This is iteration {iteration}. Previous iterations FAILED.
        Previous test feedback: {test_feedback}
        Previous failure patterns: {previous_failures}
        
        You MUST:
        1. Analyze WHY previous fixes failed
        2. Identify DIFFERENT bugs or make MORE COMPREHENSIVE fixes
        3. Don't repeat the same approach if tests are still failing
        4. Look for fundamental algorithmic issues, not just surface fixes
        """
        
        advanced_fix_result = await Runner.run(advanced_bug_fixer, advanced_fix_prompt)
        advanced_fix_output = advanced_fix_result.final_output
        print(f"Advanced Fix Implementation:")
        print(advanced_fix_output)
        
        # Step 3: Advanced evaluation with ReAct
        print(f"Running advanced ReAct evaluation...")
        advanced_eval_result = await Runner.run(
            advanced_evaluator,
            f"Use ReAct methodology to comprehensively test and evaluate the fixed version of '{program_name}'. Provide detailed failure analysis and specific actionable recommendations."
        )
        advanced_eval_output = advanced_eval_result.final_output
        print(f"Advanced Evaluation:")
        print(advanced_eval_output)
        
        # Check results
        try:
            eval_data = json.loads(advanced_eval_output)
            validation_passed = eval_data.get("validation_passed", False)
            pass_rate = eval_data.get("pass_rate", 0.0)
            
            if validation_passed:
                print(f"\nSUCCESS: Advanced approach worked! All tests passed in iteration {iteration}.")
                return {
                    "program": program_name,
                    "success": True,
                    "approach": "advanced",
                    "iterations": iteration + 1,  # +1 for simple attempt
                    "bug_analysis": advanced_bug_analysis,
                    "fix_result": advanced_fix_output,
                    "test_evaluation": advanced_eval_output
                }
            else:
                print(f"\nAdvanced iteration {iteration}: Tests failed with {pass_rate:.1%} pass rate")
                
                # Extract failure information
                failure_analysis = eval_data.get("failure_analysis", {})
                failed_cases = failure_analysis.get("failed_test_cases", [])
                failure_patterns = failure_analysis.get("failure_patterns", "")
                recommendations = eval_data.get("actionable_recommendations", [])
                
                # Track failures
                current_failures = [case.get("test_number", 0) for case in failed_cases]
                previous_failures.append({
                    "iteration": iteration,
                    "failed_tests": current_failures,
                    "pass_rate": pass_rate
                })
                
                if iteration < max_iterations:
                    test_feedback = f"""
DETAILED FAILURE ANALYSIS FROM ITERATION {iteration}:

Pass Rate: {pass_rate:.1%}

Failed Test Cases:
{json.dumps(failed_cases, indent=2)}

Failure Patterns: {failure_patterns}

Specific Actionable Recommendations:
{json.dumps(recommendations, indent=2)}

Previous Iteration History: {previous_failures}

CRITICAL: If the same tests keep failing, you need to find DIFFERENT bugs or use a COMPLETELY DIFFERENT approach.
"""
                else:
                    print(f"FAILED: Could not fix program after {max_iterations} advanced iterations")
                    return {
                        "program": program_name,
                        "success": False,
                        "approach": "advanced",
                        "iterations": max_iterations + 1,  # +1 for simple attempt
                        "bug_analysis": advanced_bug_analysis,
                        "final_fix_result": advanced_fix_output,
                        "final_test_evaluation": advanced_eval_output,
                        "failure_history": previous_failures
                    }
        except json.JSONDecodeError:
            print(f"Warning: Could not parse advanced evaluation JSON")
            if iteration >= max_iterations:
                print(f"FAILED: Could not fix program after {max_iterations} advanced iterations")
                return {
                    "program": program_name,
                    "success": False,
                    "approach": "advanced",
                    "iterations": max_iterations + 1,
                    "bug_analysis": advanced_bug_analysis,
                    "final_fix_result": advanced_fix_output,
                    "final_test_evaluation": advanced_eval_output,
                    "failure_history": previous_failures
                }
            else:
                test_feedback = f"Previous evaluation could not be parsed (iteration {iteration}). Ensure fix is correct."
        
        iteration += 1
    
    print(f"FAILED: Could not fix program after simple + {max_iterations} advanced iterations")
    return {
        "program": program_name,
        "success": False,
        "approach": "advanced",
        "iterations": max_iterations + 1,
        "bug_analysis": advanced_bug_analysis,
        "final_fix_result": advanced_fix_output,
        "final_test_evaluation": advanced_eval_output,
        "failure_history": previous_failures
    }

# Run the program
if __name__ == "__main__":
    program_name = sys.argv[1] if len(sys.argv) > 1 else "gcd"
    max_iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    print(f"Starting hybrid analysis of program: {program_name}")
    print("Strategy: Try simple approach first, escalate to advanced if needed")
    
    try:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(analyze_and_fix_program_hybrid(program_name, max_iterations))
        
        if result:
            if result["success"]:
                approach = result["approach"]
                iterations = result["iterations"]
                print(f"\nFINAL RESULT: Successfully fixed {program_name} using {approach} approach in {iterations} total iterations")
            else:
                approach = result["approach"]
                iterations = result["iterations"]
                print(f"\nFINAL RESULT: Failed to fix {program_name} after {iterations} total iterations using {approach} approach")
                if "failure_history" in result:
                    print("Failure history:")
                    for failure in result["failure_history"]:
                        print(f"  Iteration {failure['iteration']}: {failure['pass_rate']:.1%} pass rate, failed tests: {failure['failed_tests']}")
        
        print("Analysis completed")
    except KeyboardInterrupt:
        print("Operation cancelled by user")
    except Exception as e:
        print(f"Error running analysis: {str(e)}")
        import traceback
        traceback.print_exc()