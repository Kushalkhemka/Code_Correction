import os
import subprocess
import sys
from pathlib import Path
import time
from datetime import datetime
import json
import asyncio
import logging
from main_claude import analyze_single_program, available_programs, RESULTS_DIR

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('claude_sequential_batch.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def run_sequential_batch(programs_to_run=None):
    if programs_to_run is None:
        programs_to_run = available_programs
    
    logger.info(f"Starting Sequential Batch Processing with Claude 3.7 Sonnet - {len(programs_to_run)} programs")
    print(f"\n{'='*60}")
    print(f"CLAUDE 3.7 SONNET SEQUENTIAL BATCH PROCESSING")
    print(f"{'='*60}")
    
    # Process each program sequentially
    results = []
    start_time = datetime.now()
    
    for i, program in enumerate(programs_to_run, 1):
        print(f"\nProgress: {i}/{len(programs_to_run)} ({i/len(programs_to_run)*100:.1f}%)")
        print(f"{'='*60}")
        print(f"Processing: {program}")
        print(f"{'='*60}")
        
        prog_start_time = time.time()
        
        try:
            # Run analysis for single program
            result = await analyze_single_program(program)
            results.append(result)
            
            # Print success information
            duration = time.time() - prog_start_time
            bug_type = result.get('bug_classification', 'Unknown')
            print(f"SUCCESS: {program} ({duration:.2f}s) - Bug Type: {bug_type}")
            
            # Small delay to avoid overwhelming the API
            await asyncio.sleep(2)
            
        except Exception as e:
            duration = time.time() - prog_start_time
            print(f"FAILED: {program} ({duration:.2f}s)")
            print(f"Error: {str(e)}")
            
            # Add failure to results
            results.append({
                "program": program,
                "status": "error",
                "duration_seconds": round(duration, 2),
                "error": str(e),
                "llm_used": "Claude 3.7 Sonnet",
                "timestamp": datetime.now().isoformat()
            })
    
    # Generate summary statistics
    end_time = datetime.now()
    total_duration = (end_time - start_time).total_seconds()
    
    successful = [r for r in results if r.get("status") == "success"]
    failed = [r for r in results if r.get("status") == "error"]
    
    # Bug classification statistics
    bug_stats = {}
    for result in successful:
        bug_type = result.get('bug_classification', 'Unknown')
        bug_stats[bug_type] = bug_stats.get(bug_type, 0) + 1
    
    # Create summary
    summary = {
        "llm_used": "Claude 3.7 Sonnet",
        "execution_mode": "sequential",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "total_programs": len(programs_to_run),
        "successful": len(successful),
        "failed": len(failed),
        "total_duration_seconds": round(total_duration, 2),
        "average_duration_seconds": round(total_duration / max(1, len(programs_to_run)), 2),
        "programs_per_minute": round((len(programs_to_run) / max(1, total_duration)) * 60, 2),
        "bug_classification_statistics": bug_stats,
        "successful_programs": [{"program": r["program"], "bug_type": r.get("bug_classification", "Unknown")} for r in successful],
        "failed_programs": [{"program": r["program"], "error": r.get("error", "Unknown error")} for r in failed],
        "results": results
    }
    
    # Save results
    results_file = f"claude37_sequential_batch_results_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
    results_path = RESULTS_DIR / results_file
    
    with open(results_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"\n{'='*80}")
    print("CLAUDE 3.7 SONNET SEQUENTIAL BATCH PROCESSING COMPLETE")
    print(f"{'='*80}")
    
    print(f"Results Summary:")
    print(f"   Successful: {len(successful)}")
    print(f"   Failed: {len(failed)}")
    print(f"   Total Programs: {len(programs_to_run)}")
    print(f"   Total Time: {total_duration:.2f} seconds")
    print(f"   Average per Program: {total_duration/max(1, len(programs_to_run)):.2f} seconds")
    
    if bug_stats:
        print(f"\nBUG CLASSIFICATION STATISTICS:")
        print(f"{'='*40}")
        for bug_type, count in sorted(bug_stats.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / max(1, len(successful))) * 100
            print(f"{bug_type}: {count} ({percentage:.1f}%)")
    
    print(f"\nResults saved to: {results_path}")
    
    # Show failed programs
    if failed:
        print(f"\nFailed Programs:")
        for result in failed:
            print(f"   - {result['program']}: {result.get('error', 'Unknown error')[:100]}...")
    
    return summary

def modify_main_claude_for_sonnet():
    """Creates an environment variable to indicate we want to use Claude 3.7 Sonnet"""
    os.environ["CLAUDE_MODEL"] = "claude-3-7-sonnet-20240620"
    print("Set environment to use Claude 3.7 Sonnet model")

def main():
    """Main function for sequential batch processing"""
    # Set Claude 3.7 Sonnet as the model
    modify_main_claude_for_sonnet()
    
    # Get list of programs
    programs = available_programs
    if not programs:
        logger.error("ERROR: No programs found!")
        return
    
    print(f"Found {len(programs)} programs to process:")
    for i, prog in enumerate(programs[:10], 1):
        print(f"  {i:2d}. {prog}")
    if len(programs) > 10:
        print(f"  ... and {len(programs)-10} more")
    
    # Ask for confirmation
    print(f"\nThis will run the Claude 3.7 Sonnet bug finder sequentially for each program.")
    print(f"Each program will be processed one at a time.")
    confirm = input("Continue? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Cancelled by user")
        return
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            programs_to_run = programs
        else:
            programs_to_run = [p for p in sys.argv[1:] if p in programs]
            if not programs_to_run:
                print("No valid programs specified.")
                return
    else:
        # Default: run all programs
        programs_to_run = programs
    
    print(f"Will process {len(programs_to_run)} programs sequentially with Claude 3.7 Sonnet.")
    
    # Run the async function
    try:
        asyncio.run(run_sequential_batch(programs_to_run))
    except KeyboardInterrupt:
        print("Operation cancelled by user")
    except Exception as e:
        logger.error(f"Error in batch processing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()