# fix_test_imports.py
import os
from pathlib import Path

def fix_test_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the function name (e.g., get_factors)
    function_name = file_path.stem.replace('test_', '')
    
    # Create the correct import block
    new_import = f"""import pytest
from load_testdata import load_json_testcases

if pytest.fixed:
    from fixed_programs.{function_name} import {function_name}
elif pytest.use_correct:
    from correct_python_programs.{function_name} import {function_name}
else:
    from python_programs.{function_name} import {function_name}
"""
    
    # Replace the old import section
    lines = content.split('\n')
    new_lines = []
    skip_until_testdata = True
    
    for line in lines:
        if line.startswith('testdata ='):
            skip_until_testdata = False
            new_lines.append(new_import)
        
        if not skip_until_testdata:
            new_lines.append(line)
    
    with open(file_path, 'w') as f:
        f.write('\n'.join(new_lines))

# Fix all test files
test_dir = Path('python_testcases')
for test_file in test_dir.glob('test_*.py'):
    print(f"Fixing {test_file}")
    fix_test_file(test_file)