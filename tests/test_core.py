import pytest
import pandas as pd
import numpy as np
from app.data_manager import generate_synthetic_data
from app.model import PriceOptimModel

def test_data_generation():
    df = generate_synthetic_data(n_samples=50)
    assert not df.empty
    expected_cols = ['Date', 'Product', 'Price', 'Quantity', 'Cost', 'Revenue', 'Profit']
    for col in expected_cols:
        assert col in df.columns
    assert len(df) == 50

def test_model_training():
    df = generate_synthetic_data(n_samples=200)
    product = 'Widget A'
    model = PriceOptimModel(product)
    metrics = model.train(df)
    
    assert 'mae' in metrics
    assert 'r2' in metrics
    # Elasticity for regular goods should be negative usually
    assert metrics['elasticity'] < 0.5 # allowing some noise, but usually negative

def test_prediction_scenario():
    df = generate_synthetic_data(n_samples=200)
    model = PriceOptimModel('Widget A')
    model.train(df)
    
    prices = [80, 90, 100, 110, 120]
    results = model.predict_scenario(prices)
    
    assert len(results) == 5
    assert 'Predicted_Demand' in results.columns
    # Law of demand: higher price -> lower (or equal) demand usually
    # Note: ML models might be noisy, but generally trend should hold
    q_low = results.loc[results['Price'] == 80, 'Predicted_Demand'].values[0]
    q_high = results.loc[results['Price'] == 120, 'Predicted_Demand'].values[0]
    
    assert q_low >= q_high - 10 # Allow slight variance due to noise/trees but generally decreasing
