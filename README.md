# QuixBugs Hybrid Code Refactoring System

A comprehensive AI-powered code refactoring system that uses a hybrid approach to automatically detect and fix bugs in Python programs from the QuixBugs benchmark.

## Overview

The `main_hybrid.py` system combines **simple** and **advanced** AI methodologies to provide robust bug detection and fixing capabilities:

- **Phase 1 (Simple)**: Fast track analysis using straightforward bug detection
- **Phase 2 (Advanced)**: Deep analysis using Chain of Thought reasoning and Self-Refine methodology with ReAct evaluation

## Project Structure

```
Code-Refactoring-QuixBugs/
├── main_hybrid.py                    # Main hybrid analysis system
├── python_programs/                  # Original buggy programs (40 programs)
├── correct_python_programs/          # Reference correct implementations
├── fixed_programs/                   # Output directory for fixed programs
├── json_testcases/                   # JSON test cases for most programs
├── python_testcases/                 # pytest test files
├── test_runner_native.py             # Native test runner implementation
├── .env                              # API keys configuration
├── README.md                         # Original QuixBugs documentation
└── README_HYBRID.md                  # This file
```

### Key Supporting Files

- **batch_main.py**: Batch processing system
- **main_claude.py**: Claude-specific implementation  
- **main_deepseek.py**: DeepSeek-specific implementation
- **main_enhanced_cot.py**: Enhanced Chain of Thought approach
- **sequential_batch.py**: Sequential batch processing

## Setup and Configuration

### 1. Environment Setup

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
DEEPSEEK_API_KEY=your-deepseek-api-key-here
```

### 2. Install Dependencies

```bash
pip install python-dotenv
pip install agents  # AI agents framework
pip install pytest  # For running tests
```

### 3. Verify Setup

Test your API configuration:

```bash
python test_api_key.py
```

## Usage

### Basic Usage

Analyze and fix a single program:

```bash
python main_hybrid.py <program_name> [max_iterations]
```

**Examples:**

```bash
# Fix the 'gcd' program with default 3 iterations
python main_hybrid.py gcd

# Fix the 'quicksort' program with up to 5 iterations
python main_hybrid.py quicksort 5

# Fix the 'breadth_first_search' program
python main_hybrid.py breadth_first_search
```

### Available Programs

The system includes 40 Python programs from the QuixBugs benchmark:

**Algorithmic Programs:**
- `bitcount`, `bucketsort`, `find_first_in_sorted`, `find_in_sorted`
- `flatten`, `gcd`, `get_factors`, `hanoi`, `is_valid_parenthesization`
- `kheapsort`, `knapsack`, `kth`, `lcs_length`, `levenshtein`
- `lis`, `longest_common_subsequence`, `max_sublist_sum`, `mergesort`
- `next_palindrome`, `next_permutation`, `pascal`, `possible_change`
- `powerset`, `quicksort`, `rpn_eval`, `sieve`, `sqrt`, `subsequences`
- `to_base`, `wrap`

**Graph-based Programs:**
- `breadth_first_search`, `depth_first_search`, `detect_cycle`
- `minimum_spanning_tree`, `reverse_linked_list`, `shortest_path_length`
- `shortest_path_lengths`, `shortest_paths`, `topological_ordering`

## How the Hybrid System Works

### Phase 1: Simple Analysis (Fast Track)

1. **Simple Bug Finding**: Quick analysis to identify obvious bugs
2. **Simple Bug Fixing**: Apply straightforward fixes
3. **Simple Evaluation**: Basic pass/fail testing

If all tests pass → **SUCCESS** (most programs succeed here)

If tests fail → Escalate to Phase 2

### Phase 2: Advanced Analysis (Deep Dive)

1. **Advanced Bug Analysis**: 
   - Chain of Thought reasoning
   - Algorithm understanding
   - Execution tracing
   - Root cause analysis

2. **Advanced Bug Fixing** (iterative):
   - Self-Refine methodology
   - Learn from previous failures
   - Comprehensive algorithmic fixes

3. **Advanced Evaluation**:
   - ReAct (Reasoning and Acting) methodology
   - Detailed failure analysis
   - Actionable recommendations

### Key Features

- **Adaptive Strategy**: Automatically escalates complexity as needed
- **Iterative Refinement**: Up to N iterations to fix complex bugs
- **Comprehensive Testing**: Uses native test runner with detailed feedback
- **Failure Analysis**: Tracks failure patterns across iterations
- **Multiple AI Models**: Uses o3-mini for different specialized agents

## Testing Integration

### Native Test Runner

The system uses `NativeTestRunner` which supports:

- **JSON Test Cases**: For most algorithmic programs
- **Graph Test Cases**: For graph-based programs using pytest files
- **Multiple Modes**: 
  - `buggy`: Test original buggy version
  - `correct`: Test reference correct version
  - `fixed`: Test AI-generated fixed version

### Using pytest

For manual testing, you can use pytest directly:

```bash
# Install pytest
pip install pytest

# Test a single program (buggy version)
pytest python_testcases/test_quicksort.py

# Test all programs
pytest python_testcases/

# Test correct versions
pytest --correct python_testcases/

# Include slow tests
pytest --correct --runslow python_testcases/test_knapsack.py
```

### Test Modes

- **Default**: Tests buggy versions (should fail)
- **--correct**: Tests correct reference versions (should pass)
- **--runslow**: Includes slow test cases (knapsack program)

**Note**: The `levenshtein` program has a very slow test case that is always skipped.

## Output and Results

### Success Output

```
SUCCESS: Simple approach worked! All tests passed.
FINAL RESULT: Successfully fixed gcd using simple approach in 1 total iterations
```

### Failure Output

```
FAILED: Could not fix program after simple + 3 advanced iterations
FINAL RESULT: Failed to fix quicksort after 4 total iterations using advanced approach
Failure history:
  Iteration 1: 75.0% pass rate, failed tests: [3, 7]
  Iteration 2: 87.5% pass rate, failed tests: [7]
  Iteration 3: 87.5% pass rate, failed tests: [7]
```

### Generated Files

- **Fixed Code**: `fixed_programs/<program_name>.py`
- **Logs**: Various log files for debugging

## Advanced Features

### AI Agents Architecture

The system uses specialized AI agents:

**Simple Agents:**
- `simple_bug_finder`: Quick bug detection
- `simple_bug_fixer`: Straightforward fixes
- `simple_evaluator`: Basic validation

**Advanced Agents:**
- `advanced_bug_analyzer`: Deep Chain of Thought analysis
- `advanced_bug_fixer`: Self-Refine methodology
- `advanced_evaluator`: ReAct evaluation with detailed feedback

### Tool Functions

Each agent has access to specialized tools:

- `read_code`: Read source program files
- `read_testcases`: Read test cases (JSON or graph-based)
- `write_code`: Write fixed code to output directory
- `test_code_simple`: Basic testing functionality
- `test_code_verbose`: Detailed testing with failure analysis

## Configuration Options

### Max Iterations

Control the maximum number of advanced iterations:

```bash
python main_hybrid.py gcd 5  # Up to 5 advanced iterations
```

### Model Selection

The system uses OpenAI's `o3-mini` model by default. You can modify the model in the agent definitions within `main_hybrid.py`.

## Troubleshooting

### Common Issues

1. **API Key Issues**:
   ```
   API key not found in environment variables
   ```
   Solution: Ensure `.env` file contains valid `OPENAI_API_KEY`

2. **Program Not Found**:
   ```
   ERROR: Program 'xyz' not found
   ```
   Solution: Check available programs list or verify program name spelling

3. **Test Failures**:
   ```
   Error running tests: [details]
   ```
   Solution: Check that `python_programs/` and test directories exist

### Debug Mode

For detailed debugging, examine the console output which shows:
- Each phase and iteration
- Agent outputs and reasoning
- Test results and failure analysis
- Decision points for escalation

## Performance Considerations

- **Simple programs**: Usually fixed in Phase 1 (< 30 seconds)
- **Complex programs**: May require Phase 2 (1-5 minutes per iteration)
- **Very complex programs**: May timeout or require manual intervention

### Timeout Handling

Some tests (like `knapsack` and `levenshtein`) are slow:
- Use `--runslow` flag for pytest if needed
- The system handles timeouts gracefully

## Integration with Other Systems

### Batch Processing

Use `batch_main.py` for processing multiple programs:

```bash
python batch_main.py
```

### Alternative AI Models

- **Claude**: Use `main_claude.py`
- **DeepSeek**: Use `main_deepseek.py`
- **Enhanced CoT**: Use `main_enhanced_cot.py`

## Contributing

When modifying the hybrid system:

1. **Agent Instructions**: Update agent prompts for better reasoning
2. **Tool Functions**: Add new capabilities via function tools
3. **Evaluation Logic**: Enhance the success/failure detection
4. **Model Selection**: Experiment with different AI models

## Citation

Based on the QuixBugs benchmark:
> QuixBugs: A Multi-Lingual Program Repair Benchmark Set Based on the Quixey Challenge

For questions or issues, refer to the original QuixBugs documentation in `README.md`.
