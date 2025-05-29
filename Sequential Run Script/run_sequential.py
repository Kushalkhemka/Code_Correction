import os
import sys
import json
import time
import asyncio
import traceback
from datetime import datetime
from pathlib import Path
from io import StringIO

# Import from main_hybrid.py
from main_hybrid import analyze_and_fix_program_hybrid, available_programs

class LogCapture:
    """Captures detailed logs for agent processing"""
    def __init__(self, program_name):
        self.program_name = program_name
        self.log = StringIO()
        self.start_time = time.time()
    
    def log_section(self, section_name):
        """Add a section header to the log"""
        section_header = f"\n--- {section_name} ---\n"
        print(section_header)
        self.log.write(section_header)
    
    def log_message(self, message):
        """Log a message to both console and log file"""
        print(message)
        self.log.write(message + "\n")
    
    def log_agent_output(self, agent_name, output):
        """Log agent output with proper formatting"""
        header = f"Running {agent_name}..."
        print(header)
        self.log.write(header + "\n")
        
        if agent_name.lower().endswith("finder") or agent_name.lower().endswith("analyzer"):
            result_header = "Bug Analysis Result:"
            print(result_header)
            self.log.write(result_header + "\n")
        elif agent_name.lower().endswith("fixer"):
            result_header = "Fix Result:"
            print(result_header)
            self.log.write(result_header + "\n")
        elif agent_name.lower().endswith("evaluator") or agent_name.lower().endswith("validator"):
            result_header = "Evaluation:"
            print(result_header)
            self.log.write(result_header + "\n")
        
        print(output)
        self.log.write(output + "\n\n")
    
    def get_log(self):
        """Get the complete log as a string"""
        return self.log.getvalue()
    
    def save_log(self, directory):
        """Save the log to a file"""
        file_path = directory / f"{self.program_name}_detailed_log.txt"
        with open(file_path, "w") as f:
            # Add a header with timestamp
            duration = time.time() - self.start_time
            header = f"DETAILED ANALYSIS LOG FOR {self.program_name}\n"
            header += f"Generated: {datetime.now().isoformat()}\n"
            header += f"Duration: {duration:.2f} seconds\n"
            header += "=" * 70 + "\n\n"
            
            f.write(header)
            f.write(self.log.getvalue())
        
        return file_path

async def run_all_programs_sequentially(programs_to_run, max_iterations=3, start_from=None, timeout=1800):
    """
    Run specified programs sequentially through the hybrid analysis
    
    Args:
        programs_to_run: List of program names to analyze
        max_iterations: Maximum iterations for advanced phase
        start_from: Program name to start from (skips previous programs)
        timeout: Maximum time in seconds to spend on a single program
    """
    
    print(f"\n{'='*70}")
    print(f"SEQUENTIAL HYBRID ANALYSIS")
    print(f"{'='*70}")
    print(f"Programs to run: {len(programs_to_run)}")
    print(f"Max Iterations per Program: {max_iterations}")
    print(f"Program Timeout: {timeout}s ({timeout/60:.1f}m)")
    if start_from:
        print(f"Starting from: {start_from}")
    print(f"{'='*70}\n")
    
    # Statistics tracking
    start_time = time.time()
    results = []
    successful = 0
    failed = 0
    timed_out = 0
    bug_types = {}
    
    # Create results directories
    results_dir = Path("hybrid_results")
    bug_reports_dir = Path("bug_report_o3mini")
    agent_logs_dir = Path("agent_logs_o3mini")
    
    for directory in [results_dir, bug_reports_dir, agent_logs_dir]:
        if not directory.exists():
            directory.mkdir()
            print(f"Created directory: {directory}")
    
    # Create progress tracking file
    progress_file = results_dir / "batch_progress.json"
    
    # Check for progress file to enable resuming
    skip_until = None
    if start_from:
        skip_until = start_from
    elif progress_file.exists():
        try:
            with open(progress_file, "r") as f:
                progress_data = json.load(f)
                last_completed = progress_data.get("last_completed_program")
                if last_completed:
                    try:
                        last_index = programs_to_run.index(last_completed)
                        skip_until = programs_to_run[last_index + 1] if last_index < len(programs_to_run) - 1 else None
                        if skip_until:
                            print(f"Resuming from {skip_until} (after {last_completed})")
                    except ValueError:
                        pass
        except Exception as e:
            print(f"Error reading progress file: {e}")
    
    # Check for existing results
    existing_results = {}
    if results_dir.exists():
        for result_file in results_dir.glob("*_result.json"):
            program_name = result_file.stem.replace("_result", "")
            try:
                with open(result_file, "r") as f:
                    result_data = json.load(f)
                    existing_results[program_name] = result_data
                    if result_data.get("success", False):
                        successful += 1
                    else:
                        failed += 1
            except Exception:
                pass
    
    # Update progress file function
    def update_progress(current_program, status, completed=None, total=None):
        progress_data = {
            "last_completed_program": current_program,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "completed": completed,
            "total": total,
            "successful": successful,
            "failed": failed,
            "timed_out": timed_out
        }
        with open(progress_file, "w") as f:
            json.dump(progress_data, f, indent=2)
    
    # Process programs sequentially
    skipping = skip_until is not None
    for i, program in enumerate(programs_to_run, 1):
        # Skip programs until we reach the start point
        if skipping and program != skip_until:
            print(f"Skipping {program} (already processed)")
            continue
        elif skipping and program == skip_until:
            skipping = False
        
        # Check if program already has a successful result
        if program in existing_results and existing_results[program].get("success", False):
            print(f"\n[{i}/{len(programs_to_run)}] Skipping {program} (already successful)")
            results.append(existing_results[program])
            continue
        
        print(f"\n[{i}/{len(programs_to_run)}] Processing: {program}")
        print(f"{'-'*50}")
        
        program_start = time.time()
        log_capture = LogCapture(program)
        
        try:
            # Set up a timeout task
            program_task = asyncio.create_task(process_program(program, max_iterations, log_capture))
            
            try:
                # Wait for the program to complete or timeout
                result = await asyncio.wait_for(program_task, timeout=timeout)
                
                # Track results
                if result:
                    results.append(result)
                    
                    # Update statistics
                    if result.get("success", False):
                        successful += 1
                        
                        # Extract bug type for statistics
                        bug_type = "Unknown"
                        if "bug_analysis" in result:
                            bug_analysis = result["bug_analysis"]
                            # Try to extract bug_type from JSON or text
                            try:
                                if isinstance(bug_analysis, str):
                                    # Try to extract from JSON string
                                    import re
                                    bug_match = re.search(r'"bug_type":\s*"([^"]+)"', bug_analysis)
                                    if bug_match:
                                        bug_type = bug_match.group(1)
                            except:
                                pass
                        
                        bug_types[bug_type] = bug_types.get(bug_type, 0) + 1
                    else:
                        failed += 1
                
            except asyncio.TimeoutError:
                timed_out += 1
                failed += 1
                log_capture.log_message(f"\nTIMEOUT: Program {program} exceeded the {timeout}s time limit.")
                
                # Create timeout result
                result = {
                    "program": program,
                    "success": False,
                    "approach": "timeout",
                    "error": f"Timed out after {timeout} seconds",
                    "timestamp": datetime.now().isoformat()
                }
                results.append(result)
                
                # Save timeout result
                timeout_file = results_dir / f"{program}_timeout.json"
                with open(timeout_file, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"⏱️ Timeout result saved: {timeout_file}")
            
            # Save detailed log to file regardless of outcome
            log_file = log_capture.save_log(agent_logs_dir)
            print(f"📝 Detailed log saved: {log_file}")
            
            # Update progress after each program
            update_progress(program, "completed" if result.get("success", False) else "failed", i, len(programs_to_run))
            
            # Program timing
            program_end = time.time()
            duration = program_end - program_start
            print(f"⏱️ Time taken: {duration:.2f} seconds")
            
            # Progress summary after each program
            if i < len(programs_to_run):
                elapsed = time.time() - start_time
                remaining = len(programs_to_run) - i
                avg_time = elapsed / i
                eta = avg_time * remaining
                
                print(f"\n📈 Progress: {i}/{len(programs_to_run)} ({i/len(programs_to_run)*100:.1f}%)")
                print(f"🎯 Success rate: {successful}/{i} ({successful/i*100:.1f}%)")
                print(f"⏳ Elapsed: {elapsed:.1f}s | ETA: {eta:.1f}s ({eta/60:.1f}m)")
                
                # Save intermediate summary after every 5 programs
                if i % 5 == 0:
                    save_summary(results_dir, programs_to_run, results, successful, failed, timed_out, 
                                bug_types, start_time, i, "intermediate")
        
        except Exception as e:
            failed += 1
            error_msg = str(e)
            print(f"❌ ERROR: {program} - {error_msg}")
            
            # Save error log
            error_log = {
                "program": program,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": error_msg,
                "traceback": traceback.format_exc()
            }
            
            error_log_file = agent_logs_dir / f"{program}_error_log.json"
            with open(error_log_file, "w") as f:
                json.dump(error_log, f, indent=2)
            print(f"❌ Error log saved: {error_log_file}")
            
            # Also save the partial log
            log_file = log_capture.save_log(agent_logs_dir)
            print(f"📝 Partial log saved: {log_file}")
            
            # Update progress
            update_progress(program, "error", i, len(programs_to_run))
    
    # Final summary
    save_summary(results_dir, programs_to_run, results, successful, failed, timed_out, 
                bug_types, start_time, len(programs_to_run), "final")
    
    # Clean up progress file if all programs processed successfully
    if progress_file.exists() and i >= len(programs_to_run):
        try:
            os.rename(progress_file, progress_file.with_suffix(".completed"))
            print(f"✅ All programs processed. Progress file renamed to {progress_file.with_suffix('.completed')}")
        except:
            pass
    
    return successful, failed, timed_out

async def process_program(program, max_iterations, log_capture):
    """Process a single program with detailed logging"""
    # Import required components
    from main_hybrid import (
        simple_bug_finder, simple_bug_fixer, simple_evaluator, 
        advanced_bug_analyzer, advanced_bug_fixer, advanced_evaluator, 
        Runner
    )
    
    # PHASE 1: Simple analysis
    log_capture.log_section("PHASE 1: Simple Analysis (Fast Track)")
    
    # Step 1: Simple bug finding
    bug_finder_prompt = f"Use the read_code tool to read the source code of '{program}' and read_testcases to understand expected behavior, then analyze it to find the bug."
    bug_result = await Runner.run(simple_bug_finder, bug_finder_prompt)
    bug_analysis = bug_result.final_output
    log_capture.log_agent_output("simple bug finder", bug_analysis)
    
    # Step 2: Simple bug fixing
    fix_prompt = f"Use the read_code tool to read the source code of '{program}', then fix it based on this analysis: {bug_analysis}"
    fix_result = await Runner.run(simple_bug_fixer, fix_prompt)
    fix_result_output = fix_result.final_output
    log_capture.log_agent_output("simple bug fixer", fix_result_output)
    
    # Step 3: Simple evaluation
    eval_prompt = f"Use the test_code tool to test the fixed version of '{program}' and provide simple evaluation."
    eval_result = await Runner.run(simple_evaluator, eval_prompt)
    eval_output = eval_result.final_output
    log_capture.log_agent_output("simple evaluator", eval_output)
    
    # Check if simple approach worked
    simple_success = False
    try:
        eval_data = json.loads(eval_output)
        if eval_data.get("validation_passed", False):
            simple_success = True
            log_capture.log_message(f"\nSUCCESS: Simple approach worked! All tests passed.")
        else:
            pass_rate = eval_data.get("pass_rate", 0.0)
            log_capture.log_message(f"\nSimple approach failed with {pass_rate:.1%} pass rate. Escalating to advanced mode...")
    except json.JSONDecodeError:
        log_capture.log_message(f"\nSimple approach evaluation unclear. Escalating to advanced mode...")
    
    # If simple approach worked, create result object
    if simple_success:
        result = {
            "program": program,
            "success": True,
            "approach": "simple",
            "iterations": 1,
            "bug_analysis": bug_analysis,
            "fix_result": fix_result_output,
            "test_evaluation": eval_output,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to appropriate files
        save_program_results(program, result)
        
        return result
    
    # PHASE 2: Advanced analysis
    log_capture.log_section("PHASE 2: Advanced Analysis (Deep Dive)")
    
    # Step 1: Deep bug analysis
    advanced_analysis_prompt = f"Perform a deep Chain of Thought analysis of the '{program}' program. The simple approach failed, so we need deeper analysis. Read the code, understand the algorithm, trace execution, and identify the root cause of any bugs."
    advanced_bug_result = await Runner.run(advanced_bug_analyzer, advanced_analysis_prompt)
    advanced_bug_analysis = advanced_bug_result.final_output
    log_capture.log_agent_output("advanced bug analyzer", advanced_bug_analysis)
    
    # Iterative advanced fixing
    iteration = 1
    previous_failures = []
    test_feedback = ""
    advanced_success = False
    advanced_fix_output = ""
    advanced_eval_output = ""
    
    while iteration <= max_iterations and not advanced_success:
        log_capture.log_section(f"Advanced Iteration {iteration}/{max_iterations}")
        
        # Step 2: Advanced fixing with Self-Refine
        advanced_fix_prompt = f"""
        Use Self-Refine methodology to fix the '{program}' program.
        
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
        log_capture.log_agent_output("advanced bug fixer", advanced_fix_output)
        
        # Step 3: Advanced evaluation with ReAct
        advanced_eval_prompt = f"Use ReAct methodology to comprehensively test and evaluate the fixed version of '{program}'. Provide detailed failure analysis and specific actionable recommendations."
        advanced_eval_result = await Runner.run(advanced_evaluator, advanced_eval_prompt)
        advanced_eval_output = advanced_eval_result.final_output
        log_capture.log_agent_output("advanced evaluator", advanced_eval_output)
        
        # Check results
        try:
            eval_data = json.loads(advanced_eval_output)
            validation_passed = eval_data.get("validation_passed", False)
            pass_rate = eval_data.get("pass_rate", 0.0)
            
            if validation_passed:
                log_capture.log_message(f"\nSUCCESS: Advanced approach worked! All tests passed in iteration {iteration}.")
                result = {
                    "program": program,
                    "success": True,
                    "approach": "advanced",
                    "iterations": iteration + 1,  # +1 for simple attempt
                    "bug_analysis": advanced_bug_analysis,
                    "fix_result": advanced_fix_output,
                    "test_evaluation": advanced_eval_output,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Save to appropriate files
                save_program_results(program, result)
                
                advanced_success = True
                return result
            else:
                log_capture.log_message(f"\nAdvanced iteration {iteration}: Tests failed with {pass_rate:.1%} pass rate")
                
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
                    log_capture.log_message(test_feedback)
                else:
                    log_capture.log_message(f"FAILED: Could not fix program after {max_iterations} advanced iterations")
                    result = {
                        "program": program,
                        "success": False,
                        "approach": "advanced",
                        "iterations": max_iterations + 1,  # +1 for simple attempt
                        "bug_analysis": advanced_bug_analysis,
                        "final_fix_result": advanced_fix_output,
                        "final_test_evaluation": advanced_eval_output,
                        "failure_history": previous_failures,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Save to appropriate files
                    save_program_results(program, result)
                    
                    return result
        except json.JSONDecodeError:
            log_capture.log_message(f"Warning: Could not parse advanced evaluation JSON")
            if iteration >= max_iterations:
                log_capture.log_message(f"FAILED: Could not fix program after {max_iterations} advanced iterations")
                result = {
                    "program": program,
                    "success": False,
                    "approach": "advanced",
                    "iterations": max_iterations + 1,
                    "bug_analysis": advanced_bug_analysis,
                    "final_fix_result": advanced_fix_output,
                    "final_test_evaluation": advanced_eval_output,
                    "failure_history": previous_failures,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Save to appropriate files
                save_program_results(program, result)
                
                return result
            else:
                test_feedback = f"Previous evaluation could not be parsed (iteration {iteration}). Ensure fix is correct."
                log_capture.log_message(test_feedback)
        
        iteration += 1
    
    # If we exited the loop without returning a result, create a failure result
    log_capture.log_message(f"FAILED: Could not fix program after simple + {max_iterations} advanced iterations")
    result = {
        "program": program,
        "success": False,
        "approach": "advanced",
        "iterations": max_iterations + 1,
        "bug_analysis": advanced_bug_analysis,
        "final_fix_result": advanced_fix_output,
        "final_test_evaluation": advanced_eval_output,
        "failure_history": previous_failures,
        "timestamp": datetime.now().isoformat()
    }
    
    # Save to appropriate files
    save_program_results(program, result)
    
    return result

def save_program_results(program, result):
    """Save program results to appropriate files"""
    # Create directories if needed
    results_dir = Path("hybrid_results")
    bug_reports_dir = Path("bug_report_o3mini")
    agent_logs_dir = Path("agent_logs_o3mini")
    
    for directory in [results_dir, bug_reports_dir, agent_logs_dir]:
        if not directory.exists():
            directory.mkdir()
    
    # 1. Save main result
    result_file = results_dir / f"{program}_result.json"
    with open(result_file, "w") as f:
        json.dump(result, f, indent=2)
    
    # 2. Save bug report
    if "bug_analysis" in result:
        bug_report_file = bug_reports_dir / f"{program}_bug_report.json"
        with open(bug_report_file, "w") as f:
            if isinstance(result["bug_analysis"], dict):
                json.dump(result["bug_analysis"], f, indent=2)
            else:
                f.write(str(result["bug_analysis"]))
    
    # 3. Save agent log
    agent_log = {
        "program": program,
        "timestamp": datetime.now().isoformat(),
        "success": result.get("success", False),
        "approach": result.get("approach", "unknown"),
        "iterations": result.get("iterations", 0),
    }
    
    # Add simple phase logs if available
    if "bug_analysis" in result and "fix_result" in result and "test_evaluation" in result:
        agent_log["simple_phase"] = {
            "bug_finder_output": result.get("bug_analysis", ""),
            "bug_fixer_output": result.get("fix_result", ""),
            "evaluator_output": result.get("test_evaluation", "")
        }
    
    # Add advanced phase logs if available
    if result.get("approach") == "advanced":
        agent_log["advanced_phase"] = {
            "analyzer_output": result.get("bug_analysis", ""),
            "fixer_output": result.get("fix_result", ""),
            "evaluator_output": result.get("test_evaluation", ""),
            "iterations": result.get("iterations", 1) - 1  # Subtract simple phase
        }
    
    agent_log_file = agent_logs_dir / f"{program}_agent_log.json"
    with open(agent_log_file, "w") as f:
        json.dump(agent_log, f, indent=2)

def save_summary(results_dir, programs_to_run, results, successful, failed, timed_out, bug_types, start_time, completed, summary_type="final"):
    """Save summary information to a file"""
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Calculate statistics
    success_rate = successful / max(1, completed) * 100
    total_programs = len(programs_to_run)
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"SEQUENTIAL HYBRID ANALYSIS {summary_type.upper()} SUMMARY")
    print(f"{'='*70}")
    print(f"Programs processed: {completed}/{total_programs} ({completed/total_programs*100:.1f}%)")
    print(f"Successful: {successful} ({success_rate:.1f}%)")
    print(f"Failed: {failed} ({failed/completed*100:.1f}% of processed)")
    print(f"Timed out: {timed_out} ({timed_out/completed*100:.1f}% of processed)")
    print(f"Total Duration: {total_duration:.2f}s ({total_duration/60:.1f}m)")
    print(f"Average per Program: {total_duration/max(1, completed):.2f}s")
    
    # Print bug type statistics
    if bug_types:
        print(f"\n📊 BUG CLASSIFICATION STATISTICS:")
        print(f"{'-'*50}")
        sorted_bugs = sorted(bug_types.items(), key=lambda x: x[1], reverse=True)
        for bug_type, count in sorted_bugs:
            percentage = (count / successful) * 100 if successful > 0 else 0
            print(f"   {bug_type}: {count} ({percentage:.1f}%)")
    
    print(f"{'='*70}")
    
    # Create summary
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    summary = {
        "timestamp": timestamp,
        "summary_type": summary_type,
        "total_programs": total_programs,
        "programs_processed": completed,
        "successful": successful,
        "failed": failed,
        "timed_out": timed_out,
        "success_rate": success_rate,
        "total_duration_seconds": total_duration,
        "average_duration_seconds": total_duration/max(1, completed),
        "programs_per_minute": (completed/total_duration) * 60 if total_duration > 0 else 0,
        "bug_classification_statistics": bug_types,
        "results": results
    }
    
    # Save summary
    summary_file = results_dir / f"sequential_summary_{summary_type}_{timestamp}.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"📄 {summary_type.capitalize()} summary saved: {summary_file}")
    
    return summary_file

if __name__ == "__main__":
    import traceback
    
    # Create argument parser
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("\nUsage:")
        print("  python run_sequential.py [options]")
        print("\nOptions:")
        print("  all                     Process all programs (default)")
        print("  <program_name>          Process a specific program")
        print("  --max-iterations <n>    Set maximum iterations (default: 3)")
        print("  --timeout <seconds>     Set timeout per program (default: 1800s/30m)")
        print("  --resume                Resume from where previous run left off")
        print("  --start-from <program>  Start processing from specified program")
        print("  --help                  Show this help message")
        print("\nExamples:")
        print("  python run_sequential.py                 # Run all programs with default settings")
        print("  python run_sequential.py gcd            # Run only the gcd program")
        print("  python run_sequential.py --max-iterations 5  # Run all programs with 5 max iterations")
        print("  python run_sequential.py --resume       # Resume from last completed program")
        print("  python run_sequential.py --start-from mergesort  # Start from mergesort program")
        sys.exit(0)
    
    # Parse command line arguments
    max_iterations = 3
    timeout = 1800  # 30 minutes default
    start_from = None
    program_name = None
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--max-iterations" and i+1 < len(sys.argv):
            try:
                max_iterations = int(sys.argv[i+1])
                i += 2
            except ValueError:
                print(f"Error: Invalid value for --max-iterations: {sys.argv[i+1]}")
                sys.exit(1)
        elif arg == "--timeout" and i+1 < len(sys.argv):
            try:
                timeout = int(sys.argv[i+1])
                i += 2
            except ValueError:
                print(f"Error: Invalid value for --timeout: {sys.argv[i+1]}")
                sys.exit(1)
        elif arg == "--resume":
            resume = True
            i += 1
        elif arg == "--start-from" and i+1 < len(sys.argv):
            start_from = sys.argv[i+1]
            i += 2
        elif arg not in ["all", "--max-iterations", "--timeout", "--resume", "--start-from", "--help"] and not arg.startswith("--"):
            program_name = arg
            i += 1
        else:
            i += 1
    
    # Determine which programs to run
    if program_name and program_name != "all":
        # Verify the program exists
        if program_name not in available_programs:
            print(f"Error: Program '{program_name}' not found in available programs.")
            print(f"Available programs: {available_programs}")
            sys.exit(1)
            
        programs_to_run = [program_name]
        print(f"Running analysis for single program: {program_name}")
    else:
        programs_to_run = available_programs
        print(f"Running analysis for all {len(available_programs)} programs")
    
    # Verify start_from program if specified
    if start_from and start_from not in available_programs:
        print(f"Error: Start program '{start_from}' not found in available programs.")
        print(f"Available programs: {available_programs}")
        sys.exit(1)
    
    # Show configuration
    print(f"Configuration:")
    print(f"  Max iterations: {max_iterations}")
    print(f"  Timeout per program: {timeout}s ({timeout/60:.1f}m)")
    if start_from:
        print(f"  Starting from: {start_from}")
    
    # Confirm if running many programs
    if len(programs_to_run) > 5:
        estimated_time = len(programs_to_run) * 5 * 60  # Rough estimate: 5 minutes per program
        estimated_hours = estimated_time / 3600
        confirm = input(f"\nYou are about to process {len(programs_to_run)} programs sequentially.\n"
                        f"This may take approximately {estimated_hours:.1f} hours to complete.\n"
                        f"This process will consume API tokens.\n\n"
                        f"Continue? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Cancelled by user.")
            sys.exit(0)
    
    # Run the sequential analysis
    try:
        successful, failed, timed_out = asyncio.run(
            run_all_programs_sequentially(
                programs_to_run, 
                max_iterations=max_iterations,
                start_from=start_from,
                timeout=timeout
            )
        )
        
        # Final status
        print(f"\nAll processing complete!")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Timed out: {timed_out}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Analysis interrupted by user")
        print("You can resume from the last completed program using --resume")
    except Exception as e:
        print(f"\n❌ Analysis failed: {str(e)}")
        traceback.print_exc()