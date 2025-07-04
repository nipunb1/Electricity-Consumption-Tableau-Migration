#!/usr/bin/env python3
"""
Generate properly formatted Tableau workbook files (.twb) from MSTR analysis
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
from pathlib import Path
import uuid

class TableauWorkbookGenerator:
    def __init__(self, workbook_name, data_source_path):
        self.workbook_name = workbook_name
        self.data_source_path = data_source_path
        self.workbook = self._create_base_workbook()
    
    def _create_base_workbook(self):
        """Create base Tableau workbook XML structure with proper schema"""
        workbook = ET.Element('workbook', {
            'source-build': '20231.23.0213.1530',
            'source-platform': 'win',
            'version': '18.1',
            'xmlns:user': 'http://www.tableausoftware.com/xml/user'
        })
        
        document_format = ET.SubElement(workbook, 'document-format-change-manifest')
        ET.SubElement(document_format, 'IntuitiveSorting', {'UAC': 'false'})
        ET.SubElement(document_format, 'IntuitiveSorting_SP2', {'UAC': 'false'})
        ET.SubElement(document_format, 'SheetIdentifierTracking', {'UAC': 'false'})
        ET.SubElement(document_format, 'WindowsPersistSimpleIdentifiers', {'UAC': 'false'})
        
        preferences = ET.SubElement(workbook, 'preferences')
        
        datasources = ET.SubElement(workbook, 'datasources')
        self._add_data_source(datasources)
        
        worksheets = ET.SubElement(workbook, 'worksheets')
        
        dashboards = ET.SubElement(workbook, 'dashboards')
        
        return workbook
    
    def _add_data_source(self, datasources):
        """Add Excel data source connection with proper schema"""
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
        
        aliases = ET.SubElement(datasource, 'aliases', {'enabled': 'yes'})
        
        columns = [
            ('Date', 'date', 'dimension', 'ordinal'),
            ('Region', 'string', 'dimension', 'nominal'),
            ('Product_Category', 'string', 'dimension', 'nominal'),
            ('Sales_Channel', 'string', 'dimension', 'nominal'),
            ('Customer_Segment', 'string', 'dimension', 'nominal'),
            ('Revenue', 'real', 'measure', 'quantitative'),
            ('Units_Sold', 'integer', 'measure', 'quantitative'),
            ('Cost', 'real', 'measure', 'quantitative'),
            ('Customer_ID', 'string', 'dimension', 'nominal'),
            ('Product_ID', 'string', 'dimension', 'nominal'),
            ('Sales_Rep', 'string', 'dimension', 'nominal'),
            ('Quarter', 'string', 'dimension', 'ordinal'),
            ('Year', 'integer', 'dimension', 'ordinal'),
            ('Discount_Percent', 'real', 'measure', 'quantitative'),
            ('Profit_Margin', 'real', 'measure', 'quantitative'),
            ('Profit', 'real', 'measure', 'quantitative'),
            ('Unit_Price', 'real', 'measure', 'quantitative'),
            ('Discounted_Revenue', 'real', 'measure', 'quantitative')
        ]
        
        for col_name, col_type, role, semantic_type in columns:
            column_attrs = {
                'caption': col_name,
                'datatype': col_type,
                'name': f'[{col_name}]',
                'role': role,
                'type': semantic_type
            }
            ET.SubElement(datasource, 'column', column_attrs)
        
        layout = ET.SubElement(datasource, 'layout', {
            'dim-ordering': 'alphabetic',
            'dim-percentage': '0.5',
            'measure-ordering': 'alphabetic',
            'measure-percentage': '0.4',
            'show-structure': 'true'
        })
        
        semantic_values = ET.SubElement(datasource, 'semantic-values')
        ET.SubElement(semantic_values, 'semantic-value', {
            'key': '[Country].[Name]',
            'value': '&quot;United States&quot;'
        })
    
    def add_worksheet(self, name, chart_type='bar'):
        """Add a worksheet with proper view structure"""
        worksheets = self.workbook.find('worksheets')
        
        worksheet = ET.SubElement(worksheets, 'worksheet', {'name': name})
        
        table = ET.SubElement(worksheet, 'table')
        
        view = ET.SubElement(table, 'view')
        
        datasources = ET.SubElement(view, 'datasources')
        ET.SubElement(datasources, 'datasource', {
            'caption': 'ICG_2025',
            'name': 'federated.0123456789abcdef'
        })
        
        if chart_type == 'bar':
            self._add_bar_chart_config(view)
        elif chart_type == 'line':
            self._add_line_chart_config(view)
        elif chart_type == 'pie':
            self._add_pie_chart_config(view)
        else:
            self._add_table_config(view)
        
        self._add_view_structure(view)
    
    def _add_bar_chart_config(self, view):
        """Add bar chart configuration with proper schema"""
        datasource_dependencies = ET.SubElement(view, 'datasource-dependencies', {
            'datasource': 'federated.0123456789abcdef'
        })
        
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
        
        ET.SubElement(datasource_dependencies, 'column-instance', {
            'column': '[Region]',
            'derivation': 'None',
            'name': '[none:Region:nk]',
            'pivot': 'key',
            'type': 'nominal'
        })
        
        ET.SubElement(datasource_dependencies, 'column-instance', {
            'column': '[Revenue]',
            'derivation': 'Sum',
            'name': '[sum:Revenue:qk]',
            'pivot': 'key',
            'type': 'quantitative'
        })
        
        filter_elem = ET.SubElement(view, 'filter', {
            'class': 'categorical',
            'column': '[federated.0123456789abcdef].[none:Region:nk]'
        })
        
        sort_elem = ET.SubElement(view, 'sort', {
            'class': 'manual',
            'column': '[federated.0123456789abcdef].[none:Region:nk]',
            'direction': 'ASC'
        })
        
        perspectives = ET.SubElement(view, 'perspectives')
        
        slices = ET.SubElement(view, 'slices')
        
        aggregation = ET.SubElement(view, 'aggregation', {'value': 'true'})
    
    def _add_line_chart_config(self, view):
        """Add line chart configuration with proper schema"""
        datasource_dependencies = ET.SubElement(view, 'datasource-dependencies', {
            'datasource': 'federated.0123456789abcdef'
        })
        
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
        
        ET.SubElement(datasource_dependencies, 'column-instance', {
            'column': '[Date]',
            'derivation': 'None',
            'name': '[none:Date:ok]',
            'pivot': 'key',
            'type': 'ordinal'
        })
        
        ET.SubElement(datasource_dependencies, 'column-instance', {
            'column': '[Revenue]',
            'derivation': 'Sum',
            'name': '[sum:Revenue:qk]',
            'pivot': 'key',
            'type': 'quantitative'
        })
        
        filter_elem = ET.SubElement(view, 'filter', {
            'class': 'quantitative',
            'column': '[federated.0123456789abcdef].[sum:Revenue:qk]'
        })
        
        sort_elem = ET.SubElement(view, 'sort', {
            'class': 'manual',
            'column': '[federated.0123456789abcdef].[none:Date:ok]',
            'direction': 'ASC'
        })
        
        perspectives = ET.SubElement(view, 'perspectives')
        
        slices = ET.SubElement(view, 'slices')
        
        aggregation = ET.SubElement(view, 'aggregation', {'value': 'true'})
    
    def _add_pie_chart_config(self, view):
        """Add pie chart configuration with proper schema"""
        datasource_dependencies = ET.SubElement(view, 'datasource-dependencies', {
            'datasource': 'federated.0123456789abcdef'
        })
        
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
        
        ET.SubElement(datasource_dependencies, 'column-instance', {
            'column': '[Product_Category]',
            'derivation': 'None',
            'name': '[none:Product_Category:nk]',
            'pivot': 'key',
            'type': 'nominal'
        })
        
        ET.SubElement(datasource_dependencies, 'column-instance', {
            'column': '[Revenue]',
            'derivation': 'Sum',
            'name': '[sum:Revenue:qk]',
            'pivot': 'key',
            'type': 'quantitative'
        })
        
        filter_elem = ET.SubElement(view, 'filter', {
            'class': 'categorical',
            'column': '[federated.0123456789abcdef].[none:Product_Category:nk]'
        })
        
        sort_elem = ET.SubElement(view, 'sort', {
            'class': 'manual',
            'column': '[federated.0123456789abcdef].[none:Product_Category:nk]',
            'direction': 'ASC'
        })
        
        perspectives = ET.SubElement(view, 'perspectives')
        
        slices = ET.SubElement(view, 'slices')
        
        aggregation = ET.SubElement(view, 'aggregation', {'value': 'true'})
    
    def _add_table_config(self, view):
        """Add table configuration with proper schema"""
        datasource_dependencies = ET.SubElement(view, 'datasource-dependencies', {
            'datasource': 'federated.0123456789abcdef'
        })
        
        columns = [
            ('Region', 'string', 'dimension', 'nominal'),
            ('Product_Category', 'string', 'dimension', 'nominal'),
            ('Revenue', 'real', 'measure', 'quantitative'),
            ('Units_Sold', 'integer', 'measure', 'quantitative'),
            ('Profit', 'real', 'measure', 'quantitative')
        ]
        
        for col, col_type, role, semantic_type in columns:
            ET.SubElement(datasource_dependencies, 'column', {
                'caption': col,
                'datatype': col_type,
                'name': f'[{col}]',
                'role': role,
                'type': semantic_type
            })
            
            derivation = 'None' if role == 'dimension' else 'Sum'
            instance_name = f'[none:{col}:nk]' if role == 'dimension' else f'[sum:{col}:qk]'
            ET.SubElement(datasource_dependencies, 'column-instance', {
                'column': f'[{col}]',
                'derivation': derivation,
                'name': instance_name,
                'pivot': 'key',
                'type': semantic_type
            })
        
        filter_elem = ET.SubElement(view, 'filter', {
            'class': 'categorical',
            'column': '[federated.0123456789abcdef].[none:Region:nk]'
        })
        
        sort_elem = ET.SubElement(view, 'sort', {
            'class': 'manual',
            'column': '[federated.0123456789abcdef].[none:Region:nk]',
            'direction': 'ASC'
        })
        
        perspectives = ET.SubElement(view, 'perspectives')
        
        slices = ET.SubElement(view, 'slices')
        
        aggregation = ET.SubElement(view, 'aggregation', {'value': 'true'})
    
    def _add_view_structure(self, view):
        """Add required view structure elements"""
        style = ET.SubElement(view, 'style')
        
        panes = ET.SubElement(view, 'panes')
        pane = ET.SubElement(panes, 'pane', {
            'selection-relaxation-option': 'selection-relaxation-allow'
        })
        
        mark_layout = ET.SubElement(view, 'mark-layout')
        
        rows = ET.SubElement(view, 'rows')
        
        cols = ET.SubElement(view, 'cols')
    
    def add_dashboard(self, name, worksheet_names):
        """Add a dashboard with proper zone structure"""
        dashboards = self.workbook.find('dashboards')
        
        dashboard = ET.SubElement(dashboards, 'dashboard', {'name': name})
        
        size = ET.SubElement(dashboard, 'size', {
            'maxheight': '800',
            'maxwidth': '1200',
            'minheight': '800',
            'minwidth': '1200'
        })
        
        zones = ET.SubElement(dashboard, 'zones')
        
        for i, worksheet_name in enumerate(worksheet_names):
            zone_id = str(uuid.uuid4())
            zone = ET.SubElement(zones, 'zone', {
                'h': '400',
                'w': '600',
                'x': str((i % 2) * 600),
                'y': str((i // 2) * 400),
                'id': zone_id
            })
            
            zone_style = ET.SubElement(zone, 'zone-style')
            
            flipboard = ET.SubElement(zone, 'flipboard', {
                'active-id': '0',
                'auto-hide-nav': 'false'
            })
            story_point = ET.SubElement(flipboard, 'story-point', {'id': '0'})
            ET.SubElement(story_point, 'worksheet', {'name': worksheet_name})
    
    def save_workbook(self, output_path):
        """Save the workbook to a .twb file with proper formatting"""
        rough_string = ET.tostring(self.workbook, 'unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        
        print(f"Saved Tableau workbook: {output_path}")

def create_tableau_workbooks():
    """Create properly formatted Tableau workbooks for both MSTR reports"""
    
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
    
    dashboard_wb.add_dashboard('Main Dashboard', [
        'Revenue by Region', 'Revenue Trend', 'Product Performance', 'Sales Summary'
    ])
    
    dashboard_wb.save_workbook('/home/ubuntu/MSAKDashboard.twb')
    
    case2_wb = TableauWorkbookGenerator('MSAKCase2', data_source_path)
    
    case2_wb.add_worksheet('Channel Analysis', 'bar')
    case2_wb.add_worksheet('Customer Segments', 'pie')
    case2_wb.add_worksheet('Profit Analysis', 'line')
    case2_wb.add_worksheet('Detailed Report', 'table')
    
    case2_wb.add_dashboard('Case2 Dashboard', [
        'Channel Analysis', 'Customer Segments', 'Profit Analysis', 'Detailed Report'
    ])
    
    case2_wb.save_workbook('/home/ubuntu/MSAKCase2.twb')
    
    print("Created properly formatted Tableau workbooks:")
    print("- MSAKDashboard.twb")
    print("- MSAKCase2.twb")

if __name__ == "__main__":
    create_tableau_workbooks()
