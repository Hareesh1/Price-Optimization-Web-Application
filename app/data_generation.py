
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_retail_data(n_rows=2500):
    np.random.seed(42)
    random.seed(42)

    # 1. Constants & Categories
    BRANDS = ['Zara', 'H&M', 'Forever21', 'Mango', 'Uniqlo', 'Gap', 'Banana Republic', 'Ann Taylor']
    CATEGORIES = ['Dresses', 'Tops', 'Bottoms', 'Outerwear', 'Shoes', 'Accessories']
    SEASONS = ['Spring', 'Summer', 'Fall', 'Winter']
    SIZES = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
    COLORS = ['Black', 'White', 'Navy', 'Gray', 'Beige', 'Red', 'Blue', 'Green', 'Pink', 'Brown', 'Purple']
    RETURN_REASONS = ['Size Issue', 'Quality Issue', 'Color Mismatch', 'Damaged', 'Changed Mind', 'Wrong Item']

    # 2. Base Price Ranges per Category
    BASE_PRICES = {
        'Dresses': (40, 150),
        'Tops': (20, 80),
        'Bottoms': (30, 100),
        'Outerwear': (80, 250),
        'Shoes': (50, 180),
        'Accessories': (15, 60)
    }

    data = []
    
    # Generate Products (Distinct Items) first
    # Let's say we have 100 unique items per brand-category combo to make it realistic
    products = []
    for _ in range(300): # 300 unique products
        cat = random.choice(CATEGORIES)
        brand = random.choice(BRANDS)
        base_low, base_high = BASE_PRICES[cat]
        original_price = round(random.uniform(base_low, base_high), 2)
        prod_id = f"FB{str(random.randint(1, 9999)).zfill(6)}"
        
        products.append({
            'product_id': prod_id,
            'category': cat,
            'brand': brand,
            'original_price': original_price
        })

    # 3. Generate Transactions
    start_date = datetime(2024, 1, 1)
    
    for i in range(n_rows):
        prod = random.choice(products)
        
        # Seasonality & Date
        # Random date within 2 years
        days_offset = random.randint(0, 700)
        purchase_date = start_date + timedelta(days=days_offset)
        month = purchase_date.month
        
        # Determine season roughly
        if month in [12, 1, 2]: season = 'Winter'
        elif month in [3, 4, 5]: season = 'Spring'
        elif month in [6, 7, 8]: season = 'Summer'
        else: season = 'Fall'
        
        # Attributes
        size = random.choice(SIZES) if prod['category'] != 'Accessories' else None
        color = random.choice(COLORS)
        
        # Pricing & Markdown
        # Seasonal logic: High markdowns at end of seasons
        markdown_pct = 0.0
        if random.random() < 0.4: # 40% chance of being on sale
            markdown_pct = random.choice([0.1, 0.2, 0.3, 0.5])
            # Higher markdown if item season != current season (simulated simplisticly)
        
        current_price = round(prod['original_price'] * (1 - markdown_pct), 2)
        
        # Return Logic
        # Rating affects return rate
        # 15% missing ratings
        rating = None
        if random.random() > 0.15:
            # Skew ratings towards 3.5 - 5
            rating = round(np.random.triangular(1, 4.5, 5), 1)
            
        # Return Probability
        # Higher if rating is low, or random chance
        return_prob = 0.05
        if rating and rating < 3.0: return_prob += 0.3
        if prod['category'] in ['Dresses', 'Shoes']: return_prob += 0.1 # Size issues common
        
        is_returned = random.random() < return_prob
        return_reason = None
        if is_returned:
            return_reason = random.choice(RETURN_REASONS)
            if prod['category'] in ['Shoes', 'Dresses'] and random.random() < 0.6:
                return_reason = 'Size Issue'
                
        # Inventory (Snapshot at time of purchase? Or current? Let's assume current stock level for that product)
        stock_quantity = random.randint(0, 50)

        row = {
            'product_id': prod['product_id'],
            'purchase_date': purchase_date.strftime("%Y-%m-%d"),
            'category': prod['category'],
            'brand': prod['brand'],
            'season': season,
            'size': size,
            'color': color,
            'stock_quantity': stock_quantity, # Current available
            'original_price': prod['original_price'],
            'markdown_percentage': markdown_pct,
            'current_price': current_price,
            'customer_rating': rating,
            'is_returned': is_returned,
            'return_reason': return_reason
        }
        data.append(row)

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    import os
    os.makedirs('data', exist_ok=True)
    print("Generating synthetic retail data...")
    df = generate_retail_data(3000)
    save_path = 'data/retail_trend_data.csv'
    df.to_csv(save_path, index=False)
    print(f"Data generated at {save_path}")
    print(df.head())
    print(df.info())
