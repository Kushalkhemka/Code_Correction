import json
import sys
import importlib.util
import traceback
from pathlib import Path

class NativeTestRunner:
    """Test runner that works without pytest module"""
    
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        
        # Graph-based programs that use python_testcases
        self.graph_programs = [
            "breadth_first_search", "depth_first_search", "detect_cycle",
            "minimum_spanning_tree", "reverse_linked_list", "shortest_path_length",
            "shortest_path_lengths", "shortest_paths", "topological_ordering"
        ]
    
    def run_test(self, program_name, mode="buggy"):
        """
        Run tests for a specific program
        
        Args:
            program_name: Name of the program to test
            mode: "buggy", "correct", or "fixed"
            
        Returns:
            dict with test results
        """
        
        if program_name in self.graph_programs:
            return self._run_graph_tests(program_name, mode)
        else:
            return self._run_json_tests(program_name, mode)
    
    def _run_json_tests(self, program_name, mode):
        """Run JSON-based tests"""
        
        # Load test cases
        json_file = self.base_dir / "json_testcases" / f"{program_name}.json"
        if not json_file.exists():
            return {
                "success": False,
                "error": f"JSON test cases not found: {json_file}",
                "passed": 0,
                "total": 0,
                "pass_rate": 0
            }
        
        # Load the program module
        try:
            if mode == "correct":
                module_path = self.base_dir / "correct_python_programs" / f"{program_name}.py"
            elif mode == "fixed":
                module_path = self.base_dir / "fixed_programs" / f"{program_name}.py"
            else:  # buggy
                module_path = self.base_dir / "python_programs" / f"{program_name}.py"
            
            if not module_path.exists():
                return {
                    "success": False,
                    "error": f"Program file not found: {module_path}",
                    "passed": 0,
                    "total": 0,
                    "pass_rate": 0
                }
            
            # Import the module
            spec = importlib.util.spec_from_file_location(program_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            func = getattr(module, program_name)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to load module: {str(e)}",
                "passed": 0,
                "total": 0,
                "pass_rate": 0
            }
        
        # Load and run test cases
        test_cases = []
        try:
            with open(json_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line:
                        try:
                            test_case = json.loads(line)
                            test_cases.append(test_case)
                        except json.JSONDecodeError as e:
                            return {
                                "success": False,
                                "error": f"Invalid JSON on line {line_num}: {str(e)}",
                                "passed": 0,
                                "total": 0,
                                "pass_rate": 0
                            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read test cases: {str(e)}",
                "passed": 0,
                "total": 0,
                "pass_rate": 0
            }
        
        # Run tests
        passed = 0
        failed_tests = []
        
        for i, test_case in enumerate(test_cases, 1):
            try:
                if len(test_case) != 2:
                    failed_tests.append(f"Test {i}: Invalid format")
                    continue
                
                inputs, expected = test_case
                
                # Call function
                if isinstance(inputs, list):
                    actual = func(*inputs)
                else:
                    actual = func(inputs)
                
                if actual == expected:
                    passed += 1
                else:
                    failed_tests.append(f"Test {i}: Expected {expected}, got {actual}")
                    
            except Exception as e:
                failed_tests.append(f"Test {i}: Exception - {str(e)}")
        
        total = len(test_cases)
        success = passed == total
        pass_rate = passed / total if total > 0 else 0
        
        return {
            "success": success,
            "passed": passed,
            "total": total,
            "pass_rate": pass_rate,
            "failed_tests": failed_tests,
            "mode": mode,
            "program": program_name,
            "test_type": "JSON"
        }
    
    def _run_graph_tests(self, program_name, mode):
        """Run graph-based tests by importing and executing test functions"""
        
        # Load test module
        test_file = self.base_dir / "python_testcases" / f"test_{program_name}.py"
        if not test_file.exists():
            return {
                "success": False,
                "error": f"Test file not found: {test_file}",
                "passed": 0,
                "total": 0,
                "pass_rate": 0
            }
        
        # Store original modules to restore later
        original_modules = {}
        modules_to_cleanup = []
        
        try:
            # Create a proper pytest mock that matches the real pytest behavior
            import types
            pytest_mock = types.ModuleType('pytest')
            
            # Set the flags based on mode - THIS IS THE KEY FIX
            pytest_mock.fixed = (mode == "fixed")
            pytest_mock.use_correct = (mode == "correct")
            
            # Add fixture-like behavior
            def fixture(func):
                return func
            pytest_mock.fixture = fixture
            
            # Store original pytest if it exists
            if 'pytest' in sys.modules:
                original_modules['pytest'] = sys.modules['pytest']
            
            # Replace with our mock
            sys.modules['pytest'] = pytest_mock
            modules_to_cleanup.append('pytest')
            
            # Add node module to path if needed
            node_file = self.base_dir / "python_testcases" / "node.py"
            if node_file.exists():
                node_spec = importlib.util.spec_from_file_location("node", node_file)
                node_module = importlib.util.module_from_spec(node_spec)
                node_spec.loader.exec_module(node_module)
                if 'node' not in sys.modules:
                    sys.modules['node'] = node_module
                    modules_to_cleanup.append('node')
            
            # Clear any cached imports of the test module
            test_module_name = f"test_{program_name}"
            if test_module_name in sys.modules:
                original_modules[test_module_name] = sys.modules[test_module_name]
                del sys.modules[test_module_name]
            
            # Also clear any cached imports of the program modules
            program_modules = [program_name]
            if mode == "fixed":
                program_modules.extend([f"fixed_programs.{program_name}"])
            elif mode == "correct":
                program_modules.extend([f"correct_python_programs.{program_name}"])
            else:
                program_modules.extend([f"python_programs.{program_name}"])
            
            for mod_name in program_modules:
                if mod_name in sys.modules:
                    original_modules[mod_name] = sys.modules[mod_name]
                    del sys.modules[mod_name]
            
            # Import the test module fresh
            spec = importlib.util.spec_from_file_location(test_module_name, test_file)
            test_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(test_module)
            
            # Find all test functions
            test_functions = []
            for name in dir(test_module):
                if name.startswith('test') and callable(getattr(test_module, name)):
                    test_functions.append(getattr(test_module, name))
            
            if not test_functions:
                return {
                    "success": False,
                    "error": "No test functions found",
                    "passed": 0,
                    "total": 0,
                    "pass_rate": 0
                }
            
            # Run tests
            passed = 0
            failed_tests = []
            
            for test_func in test_functions:
                try:
                    # Execute the test function
                    test_func()
                    passed += 1
                except AssertionError as e:
                    # Assertion failures are test failures
                    failed_tests.append(f"{test_func.__name__}: AssertionError - {str(e)}")
                except Exception as e:
                    # Other exceptions are also test failures
                    failed_tests.append(f"{test_func.__name__}: {type(e).__name__} - {str(e)}")
            
            total = len(test_functions)
            success = passed == total
            pass_rate = passed / total if total > 0 else 0
            
            return {
                "success": success,
                "passed": passed,
                "total": total,
                "pass_rate": pass_rate,
                "failed_tests": failed_tests,
                "mode": mode,
                "program": program_name,
                "test_type": "Graph"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to run graph tests: {str(e)}\n{traceback.format_exc()}",
                "passed": 0,
                "total": 0,
                "pass_rate": 0
            }
        finally:
            # Clean up: restore original modules and remove our additions
            for module_name in modules_to_cleanup:
                if module_name in sys.modules:
                    del sys.modules[module_name]
            
            # Restore original modules
            for module_name, original_module in original_modules.items():
                sys.modules[module_name] = original_module
    
    def compare_implementations(self, program_name, verbose=False):
        """Compare all three implementations"""
        
        print(f"=== Comparing implementations for {program_name} ===")
        test_type = "Graph-based" if program_name in self.graph_programs else "JSON-based"
        print(f"Test type: {test_type}\n")
        
        modes = ["buggy", "correct", "fixed"]
        results = {}
        
        for mode in modes:
            print(f"Testing {mode} version...")
            result = self.run_test(program_name, mode)
            results[mode] = result
            
            if result["success"]:
                print(f"✅ {mode.upper()}: {result['passed']}/{result['total']} tests passed ({result['pass_rate']:.1%})")
            else:
                if "error" in result:
                    print(f"❌ {mode.upper()}: Error - {result['error']}")
                else:
                    print(f"❌ {mode.upper()}: {result['passed']}/{result['total']} tests passed ({result['pass_rate']:.1%})")
                    
                    # Show failed tests
                    if result.get("failed_tests") and verbose:
                        print("   Failed tests:")
                        for failed in result["failed_tests"][:3]:  # Show first 3
                            print(f"     - {failed}")
            
            print()
        
        print(f"=== Summary ===")
        for mode in modes:
            result = results[mode]
            status = "PASS" if result["success"] else "FAIL"
            print(f"{mode.capitalize()}: {status} ({result['pass_rate']:.1%})")
        
        return results


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python test_runner_native.py <program_name> [mode] [--verbose]")
        print("Modes: buggy, correct, fixed, compare")
        print("\nAvailable programs:")
        
        base_dir = Path.cwd()
        
        # Show JSON programs
        json_dir = base_dir / "json_testcases"
        if json_dir.exists():
            json_programs = [f.stem for f in json_dir.glob("*.json")]
            print(f"JSON-based: {', '.join(sorted(json_programs[:10]))}")
            if len(json_programs) > 10:
                print(f"  ... and {len(json_programs) - 10} more")
        
        # Show graph programs
        test_dir = base_dir / "python_testcases"
        if test_dir.exists():
            graph_programs = [f.stem[5:] for f in test_dir.glob("test_*.py") 
                            if not f.name.startswith("test_test")]
            print(f"Graph-based: {', '.join(sorted(graph_programs[:10]))}")
            if len(graph_programs) > 10:
                print(f"  ... and {len(graph_programs) - 10} more")
        
        return
    
    program_name = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else "compare"
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    runner = NativeTestRunner()
    
    if mode == "compare":
        runner.compare_implementations(program_name, verbose=verbose)
    else:
        result = runner.run_test(program_name, mode)
        
        if result["success"]:
            print(f"✅ SUCCESS: {result['passed']}/{result['total']} tests passed")
        else:
            print(f"❌ FAILED: {result['passed']}/{result['total']} tests passed")
            if "error" in result:
                print(f"Error: {result['error']}")
            elif result.get("failed_tests"):
                print("Failed tests:")
                for failed in result["failed_tests"]:
                    print(f"  - {failed}")


if __name__ == "__main__":
    main()