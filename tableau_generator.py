#!/usr/bin/env python3
"""
Generate Tableau workbook files (.twb) from MSTR analysis
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
from pathlib import Path

class TableauWorkbookGenerator:
    def __init__(self, workbook_name, data_source_path):
        self.workbook_name = workbook_name
        self.data_source_path = data_source_path
        self.workbook = self._create_base_workbook()
    
    def _create_base_workbook(self):
        """Create base Tableau workbook XML structure"""
        workbook = ET.Element('workbook', {
            'version': '18.1',
            'xmlns:user': 'http://www.tableausoftware.com/xml/user'
        })
        
        preferences = ET.SubElement(workbook, 'preferences')
        
        datasources = ET.SubElement(workbook, 'datasources')
        self._add_data_source(datasources)
        
        worksheets = ET.SubElement(workbook, 'worksheets')
        
        dashboards = ET.SubElement(workbook, 'dashboards')
        
        return workbook
    
    def _add_data_source(self, datasources):
        """Add Excel data source connection"""
        datasource = ET.SubElement(datasources, 'datasource', {
            'caption': 'ICG_2025',
            'inline': 'true',
            'name': 'federated.0123456789abcdef',
            'version': '18.1'
        })
        
        connection = ET.SubElement(datasource, 'connection', {
            'class': 'excel-direct',
            'cleaning': 'no',
            'compat': 'no',
            'dataRefreshTime': '',
            'filename': self.data_source_path,
            'interpretationMode': '0',
            'password': '',
            'server': '',
            'validate': 'no'
        })
        
        relation = ET.SubElement(connection, 'relation', {
            'connection': 'excel-direct',
            'name': 'Data',
            'table': '[Data$]',
            'type': 'table'
        })
        
        columns = [
            ('Date', 'date'),
            ('Region', 'string'),
            ('Product_Category', 'string'),
            ('Sales_Channel', 'string'),
            ('Customer_Segment', 'string'),
            ('Revenue', 'real'),
            ('Units_Sold', 'integer'),
            ('Cost', 'real'),
            ('Customer_ID', 'string'),
            ('Product_ID', 'string'),
            ('Sales_Rep', 'string'),
            ('Quarter', 'string'),
            ('Year', 'integer'),
            ('Discount_Percent', 'real'),
            ('Profit_Margin', 'real'),
            ('Profit', 'real'),
            ('Unit_Price', 'real'),
            ('Discounted_Revenue', 'real')
        ]
        
        for col_name, col_type in columns:
            ET.SubElement(datasource, 'column', {
                'caption': col_name,
                'datatype': col_type,
                'name': f'[{col_name}]',
                'role': 'dimension' if col_type == 'string' else 'measure',
                'type': 'nominal' if col_type == 'string' else 'quantitative'
            })
    
    def add_worksheet(self, name, chart_type='bar'):
        """Add a worksheet with basic visualization"""
        worksheets = self.workbook.find('worksheets')
        
        worksheet = ET.SubElement(worksheets, 'worksheet', {'name': name})
        
        table = ET.SubElement(worksheet, 'table')
        
        view = ET.SubElement(table, 'view')
        
        datasources = ET.SubElement(view, 'datasources')
        ET.SubElement(datasources, 'datasource', {'caption': 'ICG_2025', 'name': 'federated.0123456789abcdef'})
        
        if chart_type == 'bar':
            self._add_bar_chart_config(view)
        elif chart_type == 'line':
            self._add_line_chart_config(view)
        elif chart_type == 'pie':
            self._add_pie_chart_config(view)
        else:
            self._add_table_config(view)
    
    def _add_bar_chart_config(self, view):
        """Add bar chart configuration"""
        datasource_dependencies = ET.SubElement(view, 'datasource-dependencies', {'datasource': 'federated.0123456789abcdef'})
        
        ET.SubElement(datasource_dependencies, 'column', {
            'caption': 'Region',
            'datatype': 'string',
            'name': '[Region]',
            'role': 'dimension',
            'type': 'nominal'
        })
        
        ET.SubElement(datasource_dependencies, 'column', {
            'caption': 'Revenue',
            'datatype': 'real',
            'name': '[Revenue]',
            'role': 'measure',
            'type': 'quantitative'
        })
        
        aggregation = ET.SubElement(view, 'aggregation', {'value': 'true'})
    
    def _add_line_chart_config(self, view):
        """Add line chart configuration"""
        datasource_dependencies = ET.SubElement(view, 'datasource-dependencies', {'datasource': 'federated.0123456789abcdef'})
        
        ET.SubElement(datasource_dependencies, 'column', {
            'caption': 'Date',
            'datatype': 'date',
            'name': '[Date]',
            'role': 'dimension',
            'type': 'ordinal'
        })
        
        ET.SubElement(datasource_dependencies, 'column', {
            'caption': 'Revenue',
            'datatype': 'real',
            'name': '[Revenue]',
            'role': 'measure',
            'type': 'quantitative'
        })
    
    def _add_pie_chart_config(self, view):
        """Add pie chart configuration"""
        datasource_dependencies = ET.SubElement(view, 'datasource-dependencies', {'datasource': 'federated.0123456789abcdef'})
        
        ET.SubElement(datasource_dependencies, 'column', {
            'caption': 'Product_Category',
            'datatype': 'string',
            'name': '[Product_Category]',
            'role': 'dimension',
            'type': 'nominal'
        })
        
        ET.SubElement(datasource_dependencies, 'column', {
            'caption': 'Revenue',
            'datatype': 'real',
            'name': '[Revenue]',
            'role': 'measure',
            'type': 'quantitative'
        })
    
    def _add_table_config(self, view):
        """Add table configuration"""
        datasource_dependencies = ET.SubElement(view, 'datasource-dependencies', {'datasource': 'federated.0123456789abcdef'})
        
        columns = ['Region', 'Product_Category', 'Revenue', 'Units_Sold', 'Profit']
        for col in columns:
            col_type = 'string' if col in ['Region', 'Product_Category'] else 'real'
            if col == 'Units_Sold':
                col_type = 'integer'
            
            ET.SubElement(datasource_dependencies, 'column', {
                'caption': col,
                'datatype': col_type,
                'name': f'[{col}]',
                'role': 'dimension' if col_type == 'string' else 'measure',
                'type': 'nominal' if col_type == 'string' else 'quantitative'
            })
    
    def add_dashboard(self, name, worksheet_names):
        """Add a dashboard that combines multiple worksheets"""
        dashboards = self.workbook.find('dashboards')
        
        dashboard = ET.SubElement(dashboards, 'dashboard', {'name': name})
        
        size = ET.SubElement(dashboard, 'size', {'maxheight': '800', 'maxwidth': '1200', 'minheight': '800', 'minwidth': '1200'})
        
        zones = ET.SubElement(dashboard, 'zones')
        
        for i, worksheet_name in enumerate(worksheet_names):
            zone = ET.SubElement(zones, 'zone', {
                'h': '400',
                'w': '600',
                'x': str((i % 2) * 600),
                'y': str((i // 2) * 400),
                'name': f'zone_{i}'
            })
            
            ET.SubElement(zone, 'zone-style')
            ET.SubElement(zone, 'zone-name', {'name': worksheet_name})
    
    def save_workbook(self, output_path):
        """Save the workbook to a .twb file"""
        rough_string = ET.tostring(self.workbook, 'unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        
        print(f"Saved Tableau workbook: {output_path}")

def create_tableau_workbooks():
    """Create Tableau workbooks for both MSTR reports"""
    
    try:
        with open('/home/ubuntu/mstr_analysis_results.json', 'r') as f:
            analysis = json.load(f)
    except FileNotFoundError:
        print("Analysis results not found. Running analysis first...")
        return
    
    data_source_path = '/home/ubuntu/ICG_2025.xlsx'
    
    dashboard_wb = TableauWorkbookGenerator('MSAKDashboard', data_source_path)
    
    dashboard_wb.add_worksheet('Revenue by Region', 'bar')
    dashboard_wb.add_worksheet('Revenue Trend', 'line')
    dashboard_wb.add_worksheet('Product Performance', 'pie')
    dashboard_wb.add_worksheet('Sales Summary', 'table')
    
    dashboard_wb.add_dashboard('Main Dashboard', ['Revenue by Region', 'Revenue Trend', 'Product Performance', 'Sales Summary'])
    
    dashboard_wb.save_workbook('/home/ubuntu/MSAKDashboard.twb')
    
    case2_wb = TableauWorkbookGenerator('MSAKCase2', data_source_path)
    
    case2_wb.add_worksheet('Channel Analysis', 'bar')
    case2_wb.add_worksheet('Customer Segments', 'pie')
    case2_wb.add_worksheet('Profit Analysis', 'line')
    case2_wb.add_worksheet('Detailed Report', 'table')
    
    case2_wb.add_dashboard('Case2 Dashboard', ['Channel Analysis', 'Customer Segments', 'Profit Analysis', 'Detailed Report'])
    
    case2_wb.save_workbook('/home/ubuntu/MSAKCase2.twb')
    
    print("Created Tableau workbooks:")
    print("- MSAKDashboard.twb")
    print("- MSAKCase2.twb")

if __name__ == "__main__":
    create_tableau_workbooks()
