import pandas as pd
import numpy as np
import datetime

def generate_synthetic_data(n_samples=1000, seed=42):
    """
    Generates synthetic sales data for pricing optimization.
    """
    np.random.seed(seed)
    
    # Dates
    start_date = datetime.date(2023, 1, 1)
    dates = [start_date + datetime.timedelta(days=i) for i in range(n_samples)]
    
    # Products
    products = ['Widget A', 'Gadget B', 'Tool C']
    product_choices = np.random.choice(products, n_samples)
    
    # Base params for each product to make data realistic
    # Product: (Base Price, Base Demand, Elasticity, Seasonality Factor)
    params = {
        'Widget A': (100, 200, -1.5, 10),
        'Gadget B': (50, 500, -2.0, 5),
        'Tool C': (200, 50, -0.8, 2)
    }
    
    data = []
    
    for date, prod in zip(dates, product_choices):
        base_price, base_volume, elasticity, noise_std = params[prod]
        
        # Random price fluctuation around base
        price_std = base_price * 0.1
        price = max(base_price * 0.5, np.random.normal(base_price, price_std))
        
        # Cost (approx 60% of base price + noise)
        cost = base_price * 0.6 + np.random.normal(0, base_price * 0.05)
        
        # Detect seasonality (e.g., higher on weekends)
        is_weekend = date.weekday() >= 5
        seasonality_mult = 1.2 if is_weekend else 1.0
        
        # Demand Function: Q = Q0 * (P/P0)^Elasticity * Seasonality + Noise
        # Linear approximation for simplicity in generation: Q = a - bP ...
        # Let's use log-log structure or simple linear for the model to pick up.
        # Linear: Q = Intercept + Slope * Price
        # Slope approx = (Elasticity * BaseVolume) / BasePrice
        
        slope = (elasticity * base_volume) / base_price
        intercept = base_volume - (slope * base_price)
        
        quantity = intercept + slope * price
        quantity = quantity * seasonality_mult
        
        # Add noise
        quantity += np.random.normal(0, noise_std)
        quantity = max(0, int(quantity)) # quantity can't be negative
        
        data.append({
            'Date': pd.to_datetime(date),
            'Product': prod,
            'Price': round(price, 2),
            'Quantity': quantity,
            'Cost': round(cost, 2)
        })
        
    df = pd.DataFrame(data)
    
    # Derived features
    df['Revenue'] = df['Price'] * df['Quantity']
    df['Profit'] = (df['Price'] - df['Cost']) * df['Quantity']
    df['Month'] = df['Date'].dt.month
    df['Weekday'] = df['Date'].dt.weekday
    df['IsWeekend'] = (df['Weekday'] >= 5).astype(int)
    
    return df

def feature_engineering(df):
    """
    Prepares data for modeling.
    """
    # Just ensure types and any additional encodings
    # For now, generate_synthetic_data does most heavy lifting
    if 'IsWeekend' not in df.columns:
        df['Weekday'] = pd.to_datetime(df['Date']).dt.weekday
        df['IsWeekend'] = (df['Weekday'] >= 5).astype(int)
    
    return df
