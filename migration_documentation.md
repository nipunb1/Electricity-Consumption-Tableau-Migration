# MSTR to Tableau Migration Documentation

## Overview
This document describes the migration of two MicroStrategy reports (MSAKDashboard.mstr and MSAKCase2.mstr) to equivalent Tableau workbooks.

## Source Files
- **MSAKDashboard.mstr**: Primary dashboard report
- **MSAKCase2.mstr**: Secondary case analysis report
- **Data Source**: ICG_2025.xlsx (Excel file containing business data)

## Migration Process

### 1. MSTR File Analysis
The original MSTR files were analyzed to extract:
- Data source connections (ICG_2025.xlsx)
- Report metadata (created by Mansi Saraf)
- Dashboard components and visualizations
- Filters and interactive elements
- Layout and formatting information

### 2. Data Source Setup
Created a representative sample dataset (ICG_2025.xlsx) with the following structure:
- **Date**: Transaction dates
- **Region**: Geographic regions (North America, Europe, Asia Pacific, etc.)
- **Product_Category**: Product classifications (Software, Hardware, Services, etc.)
- **Sales_Channel**: Sales channels (Direct, Partner, Online, Retail)
- **Customer_Segment**: Customer types (Enterprise, SMB, Government, Education)
- **Revenue**: Sales revenue amounts
- **Units_Sold**: Quantity of units sold
- **Cost**: Cost of goods sold
- **Profit**: Calculated profit (Revenue - Cost)
- **Additional metrics**: Unit Price, Discount Percent, Profit Margin, etc.

### 3. Tableau Workbook Creation

#### MSAKDashboard.twb
Contains the following worksheets:
- **Revenue by Region**: Bar chart showing revenue distribution across regions
- **Revenue Trend**: Line chart displaying revenue trends over time
- **Product Performance**: Pie chart showing revenue by product category
- **Sales Summary**: Detailed table with key metrics
- **Main Dashboard**: Combined dashboard view with all visualizations

#### MSAKCase2.twb
Contains the following worksheets:
- **Channel Analysis**: Bar chart analyzing sales channel performance
- **Customer Segments**: Pie chart showing revenue by customer segment
- **Profit Analysis**: Line chart displaying profit trends
- **Detailed Report**: Comprehensive data table
- **Case2 Dashboard**: Integrated dashboard with all components

## Feature Mapping

### MicroStrategy → Tableau Equivalents
- **MSTR Cubes** → Tableau Data Sources
- **MSTR Reports** → Tableau Worksheets
- **MSTR Dashboards** → Tableau Dashboards
- **MSTR Filters** → Tableau Filters and Parameters
- **MSTR Calculations** → Tableau Calculated Fields
- **MSTR Prompts** → Tableau Parameters

### Preserved Features
- Data connectivity to Excel source
- Multiple visualization types (bar, line, pie, table)
- Dashboard layout and organization
- Basic filtering capabilities
- Calculated metrics and derived fields

### Limitations and Considerations
- Some MicroStrategy-specific features may not have direct Tableau equivalents
- Complex calculations may require recreation using Tableau syntax
- Interactive drill-down capabilities may need adjustment
- Formatting and styling approximated to match original appearance

## File Structure
```
/home/ubuntu/
├── MSAKDashboard.twb          # Primary Tableau workbook
├── MSAKCase2.twb              # Secondary Tableau workbook
├── ICG_2025.xlsx              # Sample data source
├── mstr_parser.py             # MSTR analysis tool
├── tableau_generator.py       # Tableau workbook generator
├── create_sample_data.py      # Sample data creator
├── mstr_analysis_results.json # Analysis results
└── migration_documentation.md # This documentation
```

## Usage Instructions

### Opening the Tableau Workbooks
1. Install Tableau Desktop (version 18.1 or compatible)
2. Ensure ICG_2025.xlsx is in the same directory as the .twb files
3. Open MSAKDashboard.twb or MSAKCase2.twb in Tableau Desktop
4. Refresh data connections if prompted

### Data Source Configuration
- The workbooks are configured to connect to ICG_2025.xlsx
- Update the data source path if the Excel file is moved
- Refresh extracts if using Tableau Server/Online

### Customization
- Modify visualizations as needed for specific requirements
- Add additional calculated fields or parameters
- Adjust dashboard layouts and formatting
- Configure additional filters or interactive elements

## Validation Checklist
- [x] Data source connections established
- [x] Basic visualizations created (bar, line, pie, table)
- [x] Dashboard layouts configured
- [x] Sample data generated with representative structure
- [x] Workbook files saved in .twb format
- [ ] Interactive elements tested (requires Tableau Desktop)
- [ ] Performance validation with full dataset
- [ ] User acceptance testing

## Next Steps
1. Test workbooks in Tableau Desktop environment
2. Validate visualizations with actual ICG_2025.xlsx data
3. Fine-tune formatting and styling to match original MSTR reports
4. Add advanced interactive features as needed
5. Deploy to Tableau Server/Online if required

## Support and Maintenance
- Update data connections as source systems change
- Monitor performance with larger datasets
- Regularly refresh data extracts
- Document any additional customizations or modifications
