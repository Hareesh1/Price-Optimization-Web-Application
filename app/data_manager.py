import pandas as pd
import numpy as np
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'retail_trend_data.csv')

def load_data():
    """
    Loads the retail trend data from CSV.
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data file not found at {DATA_PATH}. Please run data_generation.py first.")
    
    df = pd.read_csv(DATA_PATH)
    
    # Ensure types
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    
    # Derived Features for Analytics
    # Revenue = current_price (since each row is a transaction)
    df['Revenue'] = df['current_price']
    
    # Margin Estimate (using original price as proxy for cost basis is tricky without cost data)
    # Let's assume Cost is roughly 40-60% of original price (randomized slightly in generation or here)
    # For consistency, let's deterministicly estimate cost so it doesn't change on reload
    np.random.seed(42)
    # create a cost map per product to be consistent
    unique_prods = df[['product_id', 'original_price']].drop_duplicates()
    unique_prods['cost_price'] = unique_prods['original_price'] * 0.4 # 60% markup
    
    df = df.merge(unique_prods[['product_id', 'cost_price']], on='product_id', how='left')
    
    df['Profit'] = df['Revenue'] - df['cost_price']
    df['Margin'] = (df['Profit'] / df['Revenue']) * 100
    
    return df

def get_filter_options(df):
    """
    Returns unique values for filters.
    """
    return {
        'brands': sorted(df['brand'].unique()),
        'categories': sorted(df['category'].unique()),
        'seasons': sorted(df['season'].unique()),
        'sizes': sorted(df['size'].dropna().unique())
    }
