#!/usr/bin/env python3
"""
Schema-compliant Tableau workbook generator that follows exact Tableau XML requirements
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import json

class TableauSchemaCompliantGenerator:
    def __init__(self):
        self.workbook = None
        self.datasource = None
        
    def create_base_workbook(self):
        """Create base workbook structure with proper schema compliance"""
        self.workbook = ET.Element('workbook', {
            'xmlns:user': 'http://www.tableausoftware.com/xml/user',
            'source-build': '20231.23.0213.1530',
            'source-platform': 'win',
            'version': '18.1'
        })
        
        manifest = ET.SubElement(self.workbook, 'document-format-change-manifest')
        ET.SubElement(manifest, 'IntuitiveSorting', {'UAC': 'false'})
        ET.SubElement(manifest, 'IntuitiveSorting_SP2', {'UAC': 'false'})
        ET.SubElement(manifest, 'SheetIdentifierTracking', {'UAC': 'false'})
        ET.SubElement(manifest, 'WindowsPersistSimpleIdentifiers', {'UAC': 'false'})
        
        ET.SubElement(self.workbook, 'preferences')
        
        return self.workbook
    
    def add_datasource(self, data_file_path):
        """Add properly structured datasource"""
        datasources = ET.SubElement(self.workbook, 'datasources')
        
        self.datasource = ET.SubElement(datasources, 'datasource', {
            'caption': 'ICG_2025',
            'inline': 'true',
            'name': 'federated.0123456789abcdef',
            'version': '18.1'
        })
        
        connection = ET.SubElement(self.datasource, 'connection', {
            'class': 'excel-direct',
            'cleaning': 'no',
            'compat': 'no',
            'dataRefreshTime': '',
            'filename': data_file_path,
            'interpretationMode': '0',
            'password': '',
            'server': '',
            'validate': 'no'
        })
        
        ET.SubElement(connection, 'relation', {
            'connection': 'excel-direct',
            'name': 'Data',
            'table': '[Data$]',
            'type': 'table'
        })
        
        ET.SubElement(self.datasource, 'aliases', {'enabled': 'yes'})
        
        columns = [
            {'name': '[Date]', 'caption': 'Date', 'datatype': 'date', 'role': 'dimension', 'type': 'ordinal'},
            {'name': '[Region]', 'caption': 'Region', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
            {'name': '[Product_Category]', 'caption': 'Product_Category', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
            {'name': '[Sales_Channel]', 'caption': 'Sales_Channel', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
            {'name': '[Customer_Segment]', 'caption': 'Customer_Segment', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
            {'name': '[Revenue]', 'caption': 'Revenue', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'},
            {'name': '[Units_Sold]', 'caption': 'Units_Sold', 'datatype': 'integer', 'role': 'measure', 'type': 'quantitative'},
            {'name': '[Cost]', 'caption': 'Cost', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'},
            {'name': '[Customer_ID]', 'caption': 'Customer_ID', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
            {'name': '[Product_ID]', 'caption': 'Product_ID', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
            {'name': '[Sales_Rep]', 'caption': 'Sales_Rep', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
            {'name': '[Quarter]', 'caption': 'Quarter', 'datatype': 'string', 'role': 'dimension', 'type': 'ordinal'},
            {'name': '[Year]', 'caption': 'Year', 'datatype': 'integer', 'role': 'dimension', 'type': 'ordinal'},
            {'name': '[Discount_Percent]', 'caption': 'Discount_Percent', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'},
            {'name': '[Profit_Margin]', 'caption': 'Profit_Margin', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'},
            {'name': '[Profit]', 'caption': 'Profit', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'},
            {'name': '[Unit_Price]', 'caption': 'Unit_Price', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'},
            {'name': '[Discounted_Revenue]', 'caption': 'Discounted_Revenue', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'}
        ]
        
        for col in columns:
            ET.SubElement(self.datasource, 'column', col)
        
        ET.SubElement(self.datasource, 'layout', {
            'dim-ordering': 'alphabetic',
            'dim-percentage': '0.5',
            'measure-ordering': 'alphabetic',
            'measure-percentage': '0.4',
            'show-structure': 'true'
        })
        
        semantic_values = ET.SubElement(self.datasource, 'semantic-values')
        ET.SubElement(semantic_values, 'semantic-value', {
            'key': '[Country].[Name]',
            'value': '&quot;United States&quot;'
        })
    
    def add_worksheet(self, name, columns, chart_type='bar'):
        """Add properly structured worksheet with minimal required elements"""
        worksheets = self.workbook.find('worksheets')
        if worksheets is None:
            worksheets = ET.SubElement(self.workbook, 'worksheets')
        
        worksheet = ET.SubElement(worksheets, 'worksheet', {'name': name})
        table = ET.SubElement(worksheet, 'table')
        view = ET.SubElement(table, 'view')
        
        datasources = ET.SubElement(view, 'datasources')
        ET.SubElement(datasources, 'datasource', {
            'caption': 'ICG_2025',
            'name': 'federated.0123456789abcdef'
        })
        
        deps = ET.SubElement(view, 'datasource-dependencies', {
            'datasource': 'federated.0123456789abcdef'
        })
        
        for col in columns:
            ET.SubElement(deps, 'column', col)
        
        ET.SubElement(view, 'aggregation', {'value': 'true'})
    
    def add_dashboard(self, name, worksheets):
        """Add properly structured dashboard with simple zones"""
        dashboards = self.workbook.find('dashboards')
        if dashboards is None:
            dashboards = ET.SubElement(self.workbook, 'dashboards')
        
        dashboard = ET.SubElement(dashboards, 'dashboard', {'name': name})
        
        ET.SubElement(dashboard, 'size', {
            'maxheight': '800',
            'maxwidth': '1200',
            'minheight': '800',
            'minwidth': '1200'
        })
        
        zones = ET.SubElement(dashboard, 'zones')
        
        zone_configs = [
            {'x': '0', 'y': '0', 'w': '600', 'h': '400'},
            {'x': '600', 'y': '0', 'w': '600', 'h': '400'},
            {'x': '0', 'y': '400', 'w': '600', 'h': '400'},
            {'x': '600', 'y': '400', 'w': '600', 'h': '400'}
        ]
        
        for i, (worksheet_name, config) in enumerate(zip(worksheets, zone_configs)):
            zone = ET.SubElement(zones, 'zone', {
                'h': config['h'],
                'w': config['w'],
                'x': config['x'],
                'y': config['y'],
                'id': str(i)  # Use simple numeric IDs
            })
            
            ET.SubElement(zone, 'zone-style')
            ET.SubElement(zone, 'zone', {'name': worksheet_name})
    
    def save_workbook(self, filename):
        """Save workbook with proper formatting"""
        rough_string = ET.tostring(self.workbook, 'unicode')
        reparsed = minidom.parseString(rough_string)
        pretty = reparsed.toprettyxml(indent="  ")
        
        lines = [line for line in pretty.split('\n') if line.strip()]
        pretty = '\n'.join(lines)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(pretty)
        
        print(f"Saved schema-compliant workbook: {filename}")

def create_schema_compliant_workbooks():
    """Create both workbooks with proper schema compliance"""
    
    generator1 = TableauSchemaCompliantGenerator()
    generator1.create_base_workbook()
    generator1.add_datasource('Data/ICG_2025.xlsx')
    
    generator1.add_worksheet('Revenue by Region', [
        {'name': '[Region]', 'caption': 'Region', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
        {'name': '[Revenue]', 'caption': 'Revenue', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'}
    ])
    
    generator1.add_worksheet('Revenue Trend', [
        {'name': '[Date]', 'caption': 'Date', 'datatype': 'date', 'role': 'dimension', 'type': 'ordinal'},
        {'name': '[Revenue]', 'caption': 'Revenue', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'}
    ])
    
    generator1.add_worksheet('Product Performance', [
        {'name': '[Product_Category]', 'caption': 'Product_Category', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
        {'name': '[Revenue]', 'caption': 'Revenue', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'}
    ])
    
    generator1.add_worksheet('Sales Summary', [
        {'name': '[Region]', 'caption': 'Region', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
        {'name': '[Product_Category]', 'caption': 'Product_Category', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
        {'name': '[Revenue]', 'caption': 'Revenue', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'},
        {'name': '[Units_Sold]', 'caption': 'Units_Sold', 'datatype': 'integer', 'role': 'measure', 'type': 'quantitative'},
        {'name': '[Profit]', 'caption': 'Profit', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'}
    ])
    
    generator1.add_dashboard('Main Dashboard', [
        'Revenue by Region', 'Revenue Trend', 'Product Performance', 'Sales Summary'
    ])
    
    generator1.save_workbook('/home/ubuntu/MSAKDashboard.twb')
    
    generator2 = TableauSchemaCompliantGenerator()
    generator2.create_base_workbook()
    generator2.add_datasource('Data/ICG_2025.xlsx')
    
    generator2.add_worksheet('Case Analysis', [
        {'name': '[Customer_Segment]', 'caption': 'Customer_Segment', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
        {'name': '[Revenue]', 'caption': 'Revenue', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'}
    ])
    
    generator2.add_worksheet('Channel Performance', [
        {'name': '[Sales_Channel]', 'caption': 'Sales_Channel', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'},
        {'name': '[Units_Sold]', 'caption': 'Units_Sold', 'datatype': 'integer', 'role': 'measure', 'type': 'quantitative'}
    ])
    
    generator2.add_worksheet('Profit Analysis', [
        {'name': '[Quarter]', 'caption': 'Quarter', 'datatype': 'string', 'role': 'dimension', 'type': 'ordinal'},
        {'name': '[Profit]', 'caption': 'Profit', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'}
    ])
    
    generator2.add_worksheet('Summary View', [
        {'name': '[Year]', 'caption': 'Year', 'datatype': 'integer', 'role': 'dimension', 'type': 'ordinal'},
        {'name': '[Revenue]', 'caption': 'Revenue', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'},
        {'name': '[Cost]', 'caption': 'Cost', 'datatype': 'real', 'role': 'measure', 'type': 'quantitative'}
    ])
    
    generator2.add_dashboard('Case Dashboard', [
        'Case Analysis', 'Channel Performance', 'Profit Analysis', 'Summary View'
    ])
    
    generator2.save_workbook('/home/ubuntu/MSAKCase2.twb')
    
    print("\n=== SCHEMA-COMPLIANT WORKBOOKS CREATED ===")
    print("Both workbooks generated with minimal, valid XML structure")
    print("- Removed problematic elements (flipboard, story-point, etc.)")
    print("- Used simple numeric zone IDs instead of UUIDs")
    print("- Minimal view structure to avoid content model violations")
    print("- Proper element ordering and required attributes")

if __name__ == "__main__":
    create_schema_compliant_workbooks()
