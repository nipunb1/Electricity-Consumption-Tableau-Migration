#!/usr/bin/env python3
"""
Main migration script - orchestrates the complete MSTR to Tableau migration process
"""

import subprocess
import sys
import os
from pathlib import Path

def run_script(script_path, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}:")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Run the complete migration process"""
    print("MSTR to Tableau Migration Process")
    print("=" * 50)
    
    required_files = [
        '/home/ubuntu/mstr_analysis/MSAKDashboard',
        '/home/ubuntu/mstr_analysis/MSAKCase2'
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"Error: Required path not found: {file_path}")
            print("Please ensure MSTR files have been extracted first.")
            return False
    
    if not run_script('/home/ubuntu/mstr_parser.py', "MSTR File Analysis"):
        print("Failed to analyze MSTR files. Stopping migration.")
        return False
    
    if not run_script('/home/ubuntu/create_sample_data.py', "Sample Data Creation"):
        print("Failed to create sample data. Stopping migration.")
        return False
    
    if not run_script('/home/ubuntu/tableau_generator.py', "Tableau Workbook Generation"):
        print("Failed to generate Tableau workbooks. Stopping migration.")
        return False
    
    output_files = [
        '/home/ubuntu/MSAKDashboard.twb',
        '/home/ubuntu/MSAKCase2.twb',
        '/home/ubuntu/ICG_2025.xlsx',
        '/home/ubuntu/mstr_analysis_results.json'
    ]
    
    print(f"\n{'='*50}")
    print("Migration Complete - Verifying Output Files")
    print(f"{'='*50}")
    
    all_files_exist = True
    for file_path in output_files:
        if Path(file_path).exists():
            file_size = Path(file_path).stat().st_size
            print(f"✓ {file_path} ({file_size:,} bytes)")
        else:
            print(f"✗ {file_path} - NOT FOUND")
            all_files_exist = False
    
    if all_files_exist:
        print(f"\n{'='*50}")
        print("SUCCESS: Migration completed successfully!")
        print(f"{'='*50}")
        print("\nGenerated Files:")
        print("- MSAKDashboard.twb: Primary dashboard workbook")
        print("- MSAKCase2.twb: Secondary case analysis workbook")
        print("- ICG_2025.xlsx: Sample data source")
        print("- mstr_analysis_results.json: Detailed analysis results")
        print("- migration_documentation.md: Complete documentation")
        print("\nNext Steps:")
        print("1. Open the .twb files in Tableau Desktop")
        print("2. Verify data connections and visualizations")
        print("3. Customize as needed for specific requirements")
        return True
    else:
        print(f"\n{'='*50}")
        print("PARTIAL SUCCESS: Some files were not generated")
        print(f"{'='*50}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
