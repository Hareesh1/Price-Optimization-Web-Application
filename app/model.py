import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class RetailModelManager:
    def __init__(self):
        self.demand_model = RandomForestRegressor(n_estimators=50, random_state=42)
        self.return_model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.encoders = {}
        self.is_trained = False
        
    def prepare_features(self, df):
        """
        Encodes categorical features for ML.
        """
        data = df.copy()
        
        # Features to use
        categorical_cols = ['brand', 'category', 'season', 'size', 'color']
        numerical_cols = ['current_price', 'markdown_percentage', 'original_price']
        
        # Fill missing sizes (e.g. for accessories)
        data['size'] = data['size'].fillna('NA')
        
        # Encode
        for col in categorical_cols:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
            self.encoders[col] = le
            
        return data, categorical_cols + numerical_cols

    def train(self, df):
        """
        Trains both demand and return models.
        """
        # 1. Demand Model (Predicting Sales Volume? Or likelihood of sale?)
        # Since our data is Transactional, we aggregate to simulate "Units Sold per Product/Day"
        # For simplicity in this demo, let's predict "Daily Units Sold" based on attributes + price.
        
        # Aggregate by Date + Product
        daily_sales = df.groupby(['purchase_date', 'product_id', 'brand', 'category', 'season', 'current_price', 'markdown_percentage', 'original_price', 'size', 'color']).size().reset_index(name='units_sold')
        
        # For 'Return', we use the transactional data directly (probability of this item being returned)
        
        # Train Demand Model
        X_demand_df, features = self.prepare_features(daily_sales)
        X = X_demand_df[features]
        y = daily_sales['units_sold']
        
        self.demand_model.fit(X, y)
        
        # Train Return Model
        # Target: is_returned (boolean)
        # Use main transaction df
        X_return_df, features_ret = self.prepare_features(df)
        X_ret = X_return_df[features] # Same features
        y_ret = df['is_returned'].astype(int)
        
        self.return_model.fit(X_ret, y_ret)
        
        self.is_trained = True
        return self.demand_model.feature_importances_

    def predict_optimization(self, product_row, price_range):
        """
        Simulate demand and revenue for a range of prices for a specific product context.
        product_row: dict containing 'brand', 'category', 'season', 'size', 'color', 'original_price'
        """
        if not self.is_trained:
            raise Exception("Model not trained")
            
        results = []
        
        # Prepare base input vector
        # We need to encode the input 'product_row' using saved encoders
        input_data = product_row.copy()
        for col, le in self.encoders.items():
            if col in input_data:
                # Handle unseen labels carefully, or just try/except
                try:
                    input_data[col] = le.transform([input_data[col]])[0]
                except:
                    input_data[col] = 0 # Fallback
        
        for price in price_range:
            # Calculate markdown
            orig = input_data['original_price']
            markdown = (orig - price) / orig if orig > 0 else 0
            
            # Construct feature vector
            # Order must match training: ['brand', 'category', 'season', 'size', 'color', 'current_price', 'markdown_percentage', 'original_price']
            features = [
                input_data['brand'],
                input_data['category'],
                input_data['season'],
                input_data['size'],
                input_data['color'],
                price,
                markdown,
                input_data['original_price']
            ]
            
            # Predict Demand (Units)
            pred_demand = self.demand_model.predict([features])[0]
            # Predict Return Prob
            pred_return_prob = self.return_model.predict_proba([features])[0][1]
            
            # Heuristic adjustment: Demand shouldn't be effectively zero near 0 price, but let's trust the forest
            # Smooth it a bit
            pred_demand = max(0.01, pred_demand)
            
            revenue = price * pred_demand
            adj_revenue = revenue * (1 - pred_return_prob)
            
            results.append({
                'price': price,
                'demand': pred_demand,
                'revenue': revenue,
                'return_prob': pred_return_prob,
                'adjusted_revenue': adj_revenue
            })
            
        return pd.DataFrame(results)

    def predict_return_risk(self, product_context):
        """
        Predict return probability for a single item context.
        """
        if not self.is_trained: return 0.0
        # ... logic similar to above ...
        # Simplified for now
        return 0.15 # Placeholder
