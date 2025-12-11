import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

class PriceOptimModel:
    def __init__(self, product_name):
        self.product_name = product_name
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        # Using Linear Regression for explicit elasticity calculation if needed
        self.elasticity_model = LinearRegression()
        self.metrics = {}
        
    def train(self, df):
        """
        Trains the demand forecasting model for a specific product.
        """
        # Filter for this product
        product_data = df[df['Product'] == self.product_name].copy()
        
        if product_data.empty:
            raise ValueError(f"No data found for product: {self.product_name}")
            
        features = ['Price', 'IsWeekend', 'Month']
        target = 'Quantity'
        
        X = product_data[features]
        y = product_data[target]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        # Calculate metrics
        predictions = self.model.predict(X_test)
        self.metrics['mae'] = mean_absolute_error(y_test, predictions)
        self.metrics['r2'] = r2_score(y_test, predictions)
        
        # Train simple log-log model for elasticity estimation
        # ln(Q) = alpha + beta * ln(P)
        # We handle zero quantities by adding small epsilon or filtering
        valid_idx = (y_train > 0) & (X_train['Price'] > 0)
        if valid_idx.sum() > 10:
            log_q = np.log(y_train[valid_idx])
            log_p = np.log(X_train.loc[valid_idx, 'Price']).values.reshape(-1, 1)
            self.elasticity_model.fit(log_p, log_q)
            self.metrics['elasticity'] = self.elasticity_model.coef_[0]
        else:
            self.metrics['elasticity'] = 0.0
            
        return self.metrics

    def predict_scenario(self, price_range, fixed_features=None):
        """
        Simulate demand + revenue + profit over a range of prices.
        fixed_features should be a dict like {'IsWeekend': 0, 'Month': 5}
        Defaults to mean/mode if not provided.
        """
        if fixed_features is None:
            # Default to "Average Day"
            fixed_features = {'IsWeekend': 0, 'Month': 6} # e.g. June weekday
            
        prices = np.array(price_range)
        n = len(prices)
        
        # Prepare input Data
        X_sim = pd.DataFrame({
            'Price': prices,
            'IsWeekend': [fixed_features.get('IsWeekend', 0)] * n,
            'Month': [fixed_features.get('Month', 6)] * n
        })
        
        predicted_demand = self.model.predict(X_sim)
        
        # Floor demand at 0
        predicted_demand = np.maximum(predicted_demand, 0)
        
        results = pd.DataFrame({
            'Price': prices,
            'Predicted_Demand': predicted_demand
        })
        
        # Calculate Revenue and Profit (assuming constant cost for simplicity or passed in)
        # To calculate profit we need cost. Getting avg cost from data might be needed 
        # but here we'll take it as an argument or just estimate
        
        return results
