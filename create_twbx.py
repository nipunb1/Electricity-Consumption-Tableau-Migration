#!/usr/bin/env python3
"""
Create .twbx (packaged Tableau workbook) files from .twb files and data source
"""

import zipfile
import os
import shutil
from pathlib import Path

def create_twbx_file(twb_path, data_path, output_path):
    """Create a .twbx file by packaging .twb file with data source"""
    
    temp_dir = Path("/tmp/twbx_temp")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    data_dir = temp_dir / "Data"
    data_dir.mkdir()
    
    data_file_name = Path(data_path).name
    shutil.copy2(data_path, data_dir / data_file_name)
    
    with open(twb_path, 'r', encoding='utf-8') as f:
        twb_content = f.read()
    
    twb_content = twb_content.replace(
        f'filename="{data_path}"',
        f'filename="Data/{data_file_name}"'
    )
    
    twb_file_name = Path(twb_path).name
    with open(temp_dir / twb_file_name, 'w', encoding='utf-8') as f:
        f.write(twb_content)
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(temp_dir / twb_file_name, twb_file_name)
        
        zipf.write(data_dir / data_file_name, f"Data/{data_file_name}")
    
    shutil.rmtree(temp_dir)
    
    print(f"Created {output_path}")
    return True

def main():
    """Create .twbx files for both workbooks"""
    
    data_path = "/home/ubuntu/ICG_2025.xlsx"
    
    workbooks = [
        {
            'twb': "/home/ubuntu/MSAKDashboard.twb",
            'twbx': "/home/ubuntu/MSAKDashboard.twbx"
        },
        {
            'twb': "/home/ubuntu/MSAKCase2.twb", 
            'twbx': "/home/ubuntu/MSAKCase2.twbx"
        }
    ]
    
    if not Path(data_path).exists():
        print(f"Error: Data file not found: {data_path}")
        return False
    
    success_count = 0
    for wb in workbooks:
        if not Path(wb['twb']).exists():
            print(f"Error: TWB file not found: {wb['twb']}")
            continue
            
        try:
            if create_twbx_file(wb['twb'], data_path, wb['twbx']):
                success_count += 1
                
                if Path(wb['twbx']).exists():
                    file_size = Path(wb['twbx']).stat().st_size
                    print(f"✓ {wb['twbx']} created successfully ({file_size:,} bytes)")
                else:
                    print(f"✗ Failed to create {wb['twbx']}")
                    
        except Exception as e:
            print(f"Error creating {wb['twbx']}: {e}")
    
    print(f"\nSummary: {success_count}/2 .twbx files created successfully")
    
    if success_count == 2:
        print("\n=== TWBX FILES READY ===")
        print("Both packaged Tableau workbooks have been created:")
        print("- MSAKDashboard.twbx: Primary dashboard with embedded data")
        print("- MSAKCase2.twbx: Secondary case analysis with embedded data")
        print("\nThese files can be shared independently without requiring separate data files.")
        return True
    else:
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
