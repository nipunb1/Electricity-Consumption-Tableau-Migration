#!/usr/bin/env python3
"""
Create sample ICG_2025.xlsx data file based on MSTR analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create representative sample data for ICG_2025.xlsx"""
    
    np.random.seed(42)
    random.seed(42)
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 6, 30)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East & Africa']
    product_categories = ['Software', 'Hardware', 'Services', 'Consulting', 'Support']
    sales_channels = ['Direct', 'Partner', 'Online', 'Retail']
    customer_segments = ['Enterprise', 'SMB', 'Government', 'Education']
    
    data = []
    for _ in range(5000):  # Generate 5000 sample records
        record = {
            'Date': random.choice(date_range),
            'Region': random.choice(regions),
            'Product_Category': random.choice(product_categories),
            'Sales_Channel': random.choice(sales_channels),
            'Customer_Segment': random.choice(customer_segments),
            'Revenue': round(random.uniform(1000, 100000), 2),
            'Units_Sold': random.randint(1, 500),
            'Cost': round(random.uniform(500, 50000), 2),
            'Customer_ID': f'CUST_{random.randint(1000, 9999)}',
            'Product_ID': f'PROD_{random.randint(100, 999)}',
            'Sales_Rep': f'Rep_{random.randint(1, 50)}',
            'Quarter': f'Q{((random.choice(date_range).month - 1) // 3) + 1}',
            'Year': random.choice(date_range).year,
            'Discount_Percent': round(random.uniform(0, 25), 1),
            'Profit_Margin': round(random.uniform(10, 40), 1)
        }
        
        record['Profit'] = round(record['Revenue'] - record['Cost'], 2)
        record['Unit_Price'] = round(record['Revenue'] / record['Units_Sold'], 2)
        record['Discounted_Revenue'] = round(record['Revenue'] * (1 - record['Discount_Percent']/100), 2)
        
        data.append(record)
    
    df = pd.DataFrame(data)
    
    df = df.sort_values('Date').reset_index(drop=True)
    
    df.to_excel('/home/ubuntu/ICG_2025.xlsx', index=False, sheet_name='Data')
    
    print(f"Created sample data file: ICG_2025.xlsx")
    print(f"Records: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    return df

if __name__ == "__main__":
    create_sample_data()
