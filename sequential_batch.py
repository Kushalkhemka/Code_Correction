import os
import subprocess
import sys
from pathlib import Path
import time
from datetime import datetime
import json

def get_program_list():
    programs_dir = Path("python_programs")
    if not programs_dir.exists():
        print(f"ERROR: Directory {programs_dir} not found!")
        return []
    
    programs = []
    for py_file in programs_dir.glob("*.py"):
        if not py_file.name.endswith("_test.py"):
            programs.append(py_file.stem)
    
    programs.sort()
    return programs

def run_single_program(program_name):
    print(f"\n{'='*60}")
    print(f"Processing: {program_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Run main.py with the program name
        result = subprocess.run(
            [sys.executable, "main.py", program_name],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per program
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"SUCCESS: {program_name} ({duration:.2f}s)")
            return {
                "program": program_name,
                "status": "success",
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        else:
            print(f"FAILED: {program_name} ({duration:.2f}s)")
            print(f"Error: {result.stderr}")
            return {
                "program": program_name,
                "status": "failed",
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "error": result.stderr
            }
            
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT: {program_name} (exceeded 5 minutes)")
        return {
            "program": program_name,
            "status": "timeout",
            "duration": 300,
            "error": "Process timed out after 5 minutes"
        }
    except Exception as e:
        print(f"EXCEPTION: {program_name} - {str(e)}")
        return {
            "program": program_name,
            "status": "exception",
            "duration": 0,
            "error": str(e)
        }

def main():
    """Main sequential batch processing function"""
    print("Starting Sequential Batch Processing")
    print("=" * 80)
    
    # Get list of programs
    programs = get_program_list()
    if not programs:
        print("ERROR: No programs found!")
        return
    
    print(f"Found {len(programs)} programs to process:")
    for i, prog in enumerate(programs, 1):
        print(f"  {i:2d}. {prog}")
    
    # Ask for confirmation
    print(f"\nThis will run main.py sequentially for each program.")
    confirm = input("Continue? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Cancelled by user")
        return
    
    # Process each program sequentially
    results = []
    start_time = datetime.now()
    
    for i, program in enumerate(programs, 1):
        print(f"\nProgress: {i}/{len(programs)} ({i/len(programs)*100:.1f}%)")
        result = run_single_program(program)
        results.append(result)
        
        # Small delay to avoid overwhelming the API
        time.sleep(2)
    
    # Summary
    end_time = datetime.now()
    total_duration = (end_time - start_time).total_seconds()
    
    print(f"\n{'='*80}")
    print("SEQUENTIAL BATCH PROCESSING COMPLETE")
    print(f"{'='*80}")
    
    successful = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")
    timeouts = sum(1 for r in results if r["status"] == "timeout")
    exceptions = sum(1 for r in results if r["status"] == "exception")
    
    print(f"Results Summary:")
    print(f"   Successful: {successful}")
    print(f"   Failed: {failed}")
    print(f"   Timeouts: {timeouts}")
    print(f"   Exceptions: {exceptions}")
    print(f"   Total Programs: {len(programs)}")
    print(f"   Total Time: {total_duration:.2f} seconds")
    print(f"   Average per Program: {total_duration/len(programs):.2f} seconds")
    
    # Save results
    results_file = f"sequential_batch_results_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump({
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "total_duration": total_duration,
            "total_programs": len(programs),
            "successful": successful,
            "failed": failed,
            "timeouts": timeouts,
            "exceptions": exceptions,
            "results": results
        }, f, indent=2)
    
    print(f"Results saved to: {results_file}")
    
    # Show failed programs
    if failed + timeouts + exceptions > 0:
        print(f"\nFailed Programs:")
        for result in results:
            if result["status"] != "success":
                print(f"   - {result['program']}: {result['status']}")
                if "error" in result:
                    print(f"     Error: {result['error'][:100]}...")

if __name__ == "__main__":
    main()