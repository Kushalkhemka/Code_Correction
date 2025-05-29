import os
import sys
import json
import time
import asyncio
from pathlib import Path
from datetime import datetime
from main_hybrid import analyze_and_fix_program_hybrid, available_programs

# Configuration
MAX_CONCURRENT = 10  # Adjust based on your API rate limits and CPU capacity
MAX_ITERATIONS = 3   # Default max iterations per program
RESULTS_DIR = Path(os.path.abspath(os.path.dirname(__file__))) / "parallel_hybrid_results"

# Create results directory if it doesn't exist
if not RESULTS_DIR.exists():
    RESULTS_DIR.mkdir()
    print(f"Created results directory: {RESULTS_DIR}")

async def run_parallel_analysis(programs=None, max_iterations=MAX_ITERATIONS, max_concurrent=MAX_CONCURRENT):
    """Run the hybrid analysis on multiple programs in parallel with concurrency control."""
    if programs is None:
        programs = available_programs
    
    print(f"\n{'='*80}")
    print(f"PARALLEL HYBRID ANALYSIS")
    print(f"{'='*80}")
    print(f"Total Programs: {len(programs)}")
    print(f"Max Iterations per Program: {max_iterations}")
    print(f"Max Concurrent Tasks: {max_concurrent}")
    print(f"Strategy: Simple first, then Advanced if needed")
    print(f"{'='*80}\n")
    
    # Setup for progress tracking
    start_time = time.time()
    results = []
    completed = 0
    total = len(programs)
    successful = 0
    failed = 0
    bug_stats = {}
    
    # Create semaphore to limit concurrency
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def run_with_semaphore(program):
        nonlocal completed, successful, failed
        
        async with semaphore:
            print(f"Starting analysis of {program}...")
            program_start = time.time()
            
            try:
                result = await analyze_and_fix_program_hybrid(program, max_iterations)
                program_end = time.time()
                duration = program_end - program_start
                
                # Add duration to result
                if result:
                    result["duration_seconds"] = round(duration, 2)
                    
                    # Track statistics
                    if result.get("success", False):
                        successful += 1
                        # Extract bug type if available
                        bug_type = "Unknown"
                        try:
                            bug_analysis = result.get("bug_analysis", "")
                            if isinstance(bug_analysis, str) and "bug_type" in bug_analysis:
                                import re
                                bug_type_match = re.search(r'"bug_type":\s*"([^"]+)"', bug_analysis)
                                if bug_type_match:
                                    bug_type = bug_type_match.group(1)
                        except:
                            pass
                        
                        bug_stats[bug_type] = bug_stats.get(bug_type, 0) + 1
                        print(f"✅ SUCCESS: {program} ({duration:.2f}s) - {result.get('approach', 'unknown')} approach")
                    else:
                        failed += 1
                        print(f"❌ FAILED: {program} ({duration:.2f}s) - {result.get('approach', 'unknown')} approach")
                    
                    # Save individual result
                    result_file = RESULTS_DIR / f"{program}_parallel_hybrid.json"
                    with open(result_file, "w") as f:
                        json.dump(result, f, indent=2)
                    
                    return result
                else:
                    failed += 1
                    print(f"❌ ERROR: {program} - No result returned")
                    return {
                        "program": program,
                        "success": False,
                        "error": "No result returned",
                        "duration_seconds": round(duration, 2)
                    }
            except Exception as e:
                program_end = time.time()
                duration = program_end - program_start
                failed += 1
                error_msg = str(e)
                print(f"❌ ERROR: {program} - {error_msg[:100]}...")
                
                error_result = {
                    "program": program,
                    "success": False,
                    "approach": "error",
                    "error": error_msg,
                    "duration_seconds": round(duration, 2)
                }
                return error_result
            finally:
                # Update progress counter
                completed += 1
                elapsed = time.time() - start_time
                avg_time = elapsed / max(1, completed)
                remaining = total - completed
                eta = avg_time * remaining
                
                # Print progress
                print(f"\n📊 Progress: {completed}/{total} ({completed/total*100:.1f}%)")
                print(f"   Success: {successful} | Failed: {failed}")
                print(f"   Elapsed: {elapsed:.1f}s | ETA: {eta:.1f}s ({eta/60:.1f}m)")
                print(f"   Current Success Rate: {(successful/completed)*100:.1f}%\n")
    
    # Create tasks for all programs
    tasks = [run_with_semaphore(program) for program in programs]
    
    # Run all tasks and collect results as they complete
    for future in asyncio.as_completed(tasks):
        result = await future
        if result:
            results.append(result)
    
    # Calculate final statistics
    end_time = time.time()
    total_duration = end_time - start_time
    success_rate = (successful / total) * 100 if total > 0 else 0
    
    # Create comprehensive summary
    summary = {
        "analysis_type": "Parallel Hybrid",
        "total_programs": total,
        "successful": successful,
        "failed": failed,
        "success_rate": round(success_rate, 2),
        "total_duration_seconds": round(total_duration, 2),
        "average_duration_seconds": round(total_duration / total, 2) if total > 0 else 0,
        "programs_per_minute": round((total / total_duration) * 60, 2) if total_duration > 0 else 0,
        "max_concurrent_tasks": max_concurrent,
        "max_iterations_per_program": max_iterations,
        "bug_classification_statistics": bug_stats,
        "timestamp": datetime.now().isoformat(),
        "successful_programs": [
            {
                "program": r["program"], 
                "approach": r.get("approach", "unknown"),
                "iterations": r.get("iterations", 0),
                "duration": r.get("duration_seconds", 0)
            } 
            for r in results if r.get("success", False)
        ],
        "failed_programs": [
            {
                "program": r["program"], 
                "approach": r.get("approach", "unknown"),
                "iterations": r.get("iterations", 0),
                "duration": r.get("duration_seconds", 0),
                "error": r.get("error", "Analysis failed")
            } 
            for r in results if not r.get("success", False)
        ]
    }
    
    # Save comprehensive summary
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    summary_file = RESULTS_DIR / f"parallel_hybrid_summary_{timestamp}.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print final summary
    print(f"\n{'='*80}")
    print(f"PARALLEL HYBRID ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"Total Programs: {total}")
    print(f"Successful: {successful} ({success_rate:.1f}%)")
    print(f"Failed: {failed} ({100 - success_rate:.1f}%)")
    print(f"Total Duration: {total_duration:.2f} seconds ({total_duration/60:.1f} minutes)")
    print(f"Average per Program: {total_duration/total:.2f} seconds")
    print(f"Processing Rate: {(total/total_duration)*60:.1f} programs/minute")
    print(f"Parallel Efficiency: {(total*avg_time)/total_duration*100:.1f}%")
    
    if bug_stats:
        print(f"\n📊 BUG CLASSIFICATION STATISTICS:")
        print(f"{'─' * 50}")
        sorted_bugs = sorted(bug_stats.items(), key=lambda x: x[1], reverse=True)
        for bug_type, count in sorted_bugs:
            percentage = (count / successful) * 100 if successful > 0 else 0
            print(f"   {bug_type}: {count} ({percentage:.1f}%)")
    
    print(f"\n📁 Results saved to: {RESULTS_DIR}")
    print(f"📄 Summary file: {summary_file}")
    print(f"{'='*80}")
    
    return summary

if __name__ == "__main__":
    # Parse command line arguments
    max_iterations = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else MAX_ITERATIONS
    max_concurrent = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else MAX_CONCURRENT
    
    # If specific programs are provided, use those instead of all available programs
    target_programs = None
    if len(sys.argv) > 1 and not sys.argv[1].isdigit():
        if sys.argv[1].lower() == "all":
            target_programs = available_programs
        else:
            target_programs = []
            for arg in sys.argv[1:]:
                if arg.isdigit():
                    break
                if arg in available_programs:
                    target_programs.append(arg)
                else:
                    print(f"Warning: Program '{arg}' not found in available programs, skipping.")
    
    if target_programs is not None and len(target_programs) == 0:
        print("No valid programs specified. Using all available programs.")
        target_programs = None
    
    # Print configuration
    programs_to_run = target_programs if target_programs is not None else available_programs
    print(f"🚀 Starting Parallel Hybrid Analysis")
    print(f"📋 Programs to process: {len(programs_to_run)}")
    print(f"🔄 Max iterations per program: {max_iterations}")
    print(f"⚡ Max concurrent tasks: {max_concurrent}")
    
    # Confirm if running many programs
    if len(programs_to_run) > 10:
        confirm = input(f"You are about to process {len(programs_to_run)} programs in parallel. This may incur API costs. Continue? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Cancelled by user.")
            sys.exit(0)
    
    # Run the parallel analysis
    try:
        asyncio.run(run_parallel_analysis(programs_to_run, max_iterations, max_concurrent))
    except KeyboardInterrupt:
        print("\n⏹️ Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()