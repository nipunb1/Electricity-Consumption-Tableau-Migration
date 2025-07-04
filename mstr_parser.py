#!/usr/bin/env python3
"""
MSTR File Parser - Extract dashboard components and structure from MicroStrategy files
"""

import os
import zipfile
import struct
import json
from pathlib import Path

def parse_mstr_info_cube(file_path):
    """Parse MSTR _info.cube file to extract metadata"""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            
        strings = []
        current_string = ""
        for byte in content:
            if 32 <= byte <= 126:  # Printable ASCII
                current_string += chr(byte)
            else:
                if len(current_string) > 3:  # Only keep strings longer than 3 chars
                    strings.append(current_string)
                current_string = ""
        
        metadata = {
            'data_sources': [s for s in strings if s.endswith('.xlsx') or s.endswith('.csv')],
            'server_info': [s for s in strings if 'server' in s.lower() or 'env-' in s],
            'authors': [s for s in strings if len(s.split()) == 2 and s[0].isupper()],
            'templates': [s for s in strings if 'template' in s.lower()],
            'all_strings': strings
        }
        
        return metadata
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return {}

def parse_mstr_delta(file_path):
    """Parse MSTR .delta file to extract report structure"""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            
        strings = []
        current_string = ""
        for byte in content:
            if 32 <= byte <= 126:  # Printable ASCII
                current_string += chr(byte)
            else:
                if len(current_string) > 3:
                    strings.append(current_string)
                current_string = ""
        
        viz_keywords = ['chart', 'graph', 'table', 'grid', 'plot', 'bar', 'line', 'pie', 'scatter']
        filter_keywords = ['filter', 'selector', 'parameter', 'prompt']
        layout_keywords = ['layout', 'panel', 'container', 'block', 'section']
        
        components = {
            'visualizations': [s for s in strings if any(kw in s.lower() for kw in viz_keywords)],
            'filters': [s for s in strings if any(kw in s.lower() for kw in filter_keywords)],
            'layout': [s for s in strings if any(kw in s.lower() for kw in layout_keywords)],
            'functions': [s for s in strings if 'function' in s.lower() or 'calculation' in s.lower()],
            'data_objects': [s for s in strings if len(s) > 10 and s.count(' ') < 3],
            'all_strings': strings
        }
        
        return components
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return {}

def analyze_mstr_reports():
    """Analyze both MSTR reports and extract their structure"""
    base_path = Path("/home/ubuntu/mstr_analysis")
    
    reports = {
        'MSAKDashboard': {},
        'MSAKCase2': {}
    }
    
    dashboard_path = base_path / "MSAKDashboard/773C889F6F4E37219D51CF80DB1D1E1A"
    if dashboard_path.exists():
        info_cube = dashboard_path / "1B97A2E7C945696A79242E8AD7C483CC/6B807E04934F7E120D085A8F0EB67A47_info.cube"
        if info_cube.exists():
            reports['MSAKDashboard']['metadata'] = parse_mstr_info_cube(info_cube)
        
        delta_file = dashboard_path / "E908B40A1248D7CB515A838AFF145CFE.delta"
        if delta_file.exists():
            reports['MSAKDashboard']['components'] = parse_mstr_delta(delta_file)
    
    case2_path = base_path / "MSAKCase2/219371977C4602D44CD318B1994081E1"
    if case2_path.exists():
        info_cube = case2_path / "A2FA5C8F004A17E826E4C59817E1E5D4/2D88F1028F4A71171E66AEBCD017CD37_info.cube"
        if info_cube.exists():
            reports['MSAKCase2']['metadata'] = parse_mstr_info_cube(info_cube)
        
        delta_file = case2_path / "0B272A7FAB4C84B623753DA07D013939.delta"
        if delta_file.exists():
            reports['MSAKCase2']['components'] = parse_mstr_delta(delta_file)
    
    return reports

def create_tableau_migration_plan(reports):
    """Create a migration plan based on analyzed MSTR reports"""
    plan = {
        'data_sources': set(),
        'visualizations': [],
        'filters': [],
        'calculations': [],
        'layout_components': [],
        'migration_steps': []
    }
    
    for report_name, report_data in reports.items():
        if 'metadata' in report_data:
            plan['data_sources'].update(report_data['metadata'].get('data_sources', []))
        
        if 'components' in report_data:
            components = report_data['components']
            plan['visualizations'].extend(components.get('visualizations', []))
            plan['filters'].extend(components.get('filters', []))
            plan['calculations'].extend(components.get('functions', []))
            plan['layout_components'].extend(components.get('layout', []))
    
    plan['data_sources'] = list(plan['data_sources'])
    
    plan['migration_steps'] = [
        "1. Set up data connections to ICG_2025.xlsx",
        "2. Create Tableau workbook structure for each report",
        "3. Recreate visualizations and charts",
        "4. Implement filters and interactive elements", 
        "5. Configure dashboard layouts and formatting",
        "6. Test functionality and validate against original reports"
    ]
    
    return plan

if __name__ == "__main__":
    print("Analyzing MSTR reports...")
    reports = analyze_mstr_reports()
    
    print("\n=== ANALYSIS RESULTS ===")
    for report_name, report_data in reports.items():
        print(f"\n{report_name}:")
        if 'metadata' in report_data:
            print(f"  Data Sources: {report_data['metadata'].get('data_sources', [])}")
            print(f"  Authors: {report_data['metadata'].get('authors', [])}")
            print(f"  Server: {report_data['metadata'].get('server_info', [])}")
        
        if 'components' in report_data:
            components = report_data['components']
            print(f"  Visualizations: {len(components.get('visualizations', []))}")
            print(f"  Filters: {len(components.get('filters', []))}")
            print(f"  Functions: {len(components.get('functions', []))}")
            print(f"  Layout Components: {len(components.get('layout', []))}")
    
    migration_plan = create_tableau_migration_plan(reports)
    
    print("\n=== MIGRATION PLAN ===")
    print(f"Data Sources: {migration_plan['data_sources']}")
    print(f"Total Visualizations: {len(migration_plan['visualizations'])}")
    print(f"Total Filters: {len(migration_plan['filters'])}")
    print(f"Total Calculations: {len(migration_plan['calculations'])}")
    
    print("\nMigration Steps:")
    for step in migration_plan['migration_steps']:
        print(f"  {step}")
    
    with open('/home/ubuntu/mstr_analysis_results.json', 'w') as f:
        json.dump({
            'reports': reports,
            'migration_plan': migration_plan
        }, f, indent=2, default=str)
    
    print(f"\nDetailed analysis saved to: /home/ubuntu/mstr_analysis_results.json")
