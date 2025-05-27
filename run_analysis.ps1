# PowerShell script to run the bug finder and fixer
param(
    [string]$program = "quicksort"
)

Write-Host "Running analysis on program: $program" -ForegroundColor Green
python main.py $program
