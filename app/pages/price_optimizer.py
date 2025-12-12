
import dash
from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from app.data_manager import load_data, get_filter_options
from app.model import RetailModelManager

dash.register_page(__name__)

df = load_data()
options = get_filter_options(df)
model_manager = RetailModelManager()
# Train on load (in prod, load pickled model)
print("Training models...")
model_manager.train(df)
print("Models trained.")

layout = dbc.Container([
    html.H2("Price Optimization Engine", className="my-4"),
    
    dbc.Row([
        # Input Panel
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Configuration"),
                dbc.CardBody([
                    html.Label("Select Brand"),
                    dcc.Dropdown(id='opt-brand', options=options['brands'], value=options['brands'][0]),
                    html.Br(),
                    
                    html.Label("Select Category"),
                    dcc.Dropdown(id='opt-category', options=options['categories'], value=options['categories'][0]),
                    html.Br(),
                    
                    html.Label("Season Context"),
                    dcc.Dropdown(id='opt-season', options=options['seasons'], value='Summer'),
                    html.Br(),
                    
                    html.Label("Base Price ($)"),
                    dbc.Input(id='opt-base-price', type='number', value=100),
                    html.Br(),
                    
                    dbc.Button("Run Optimization", id='btn-optimize', color="primary", className="w-100")
                ])
            ], className="shadow-sm")
        ], md=4),
        
        # Results Panel
        dbc.Col([
            dcc.Loading(
                id="loading-opt",
                children=[
                    html.Div(id='optimization-results')
                ],
                type="circle",
            )
        ], md=8)
    ])
], fluid=True)

@callback(
    Output('optimization-results', 'children'),
    Input('btn-optimize', 'n_clicks'),
    [State('opt-brand', 'value'),
     State('opt-category', 'value'),
     State('opt-season', 'value'),
     State('opt-base-price', 'value')]
)
def run_optimization(n_clicks, brand, category, season, base_price):
    if not n_clicks:
        return html.Div("Configure parameters and click Run to see optimization results.", className="text-muted text-center mt-5")
    
    # Define a generic product context
    context = {
        'brand': brand,
        'category': category,
        'season': season,
        'size': 'M', # generic default
        'color': 'Black', # generic default
        'original_price': float(base_price)
    }
    
    # Simulate Prices
    # -50% to +20% of base price
    # Wait, markdown can only go down. Usually optimization is "What is the best markdown?"
    # But user might want to optimize MSRP too.
    # Let's sweep actual price from 0.4*Base to 1.0*Base (0% to 60% off)
    price_range = np.linspace(float(base_price) * 0.4, float(base_price), 20)
    
    results_df = model_manager.predict_optimization(context, price_range)
    
    # Find Optimal
    best_row = results_df.loc[results_df['adjusted_revenue'].idxmax()]
    best_price = best_row['price']
    max_rev = best_row['adjusted_revenue']
    
    # Plot
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=results_df['price'], 
        y=results_df['adjusted_revenue'],
        mode='lines+markers',
        name='Proj. Risk-Adj Revenue',
        line=dict(shape='spline', color='#00cc96', width=4)
    ))
    
    fig.add_trace(go.Scatter(
        x=results_df['price'],
        y=results_df['revenue'],
        mode='lines',
        name='Gross Revenue',
        line=dict(dash='dot', color='gray')
    ))
    
    # Highlight Optimal
    fig.add_vline(x=best_price, line_dash="dash", line_color="white")
    fig.add_annotation(
        x=best_price, y=max_rev,
        text=f"Optimal: ${best_price:.2f}",
        showarrow=True,
        arrowhead=1
    )
    
    fig.update_layout(
        title=f"Price vs Revenue Curve for {brand} {category}",
        xaxis_title="Price ($)",
        yaxis_title="Projected Revenue ($)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified"
    )
    
    return html.Div([
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H5("Recommended Price", className="card-title"),
                    html.H2(f"${best_price:.2f}", className="text-success")
                ])
            ], className="text-center mb-3"), width=6),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H5("Proj. Revenue", className="card-title"),
                    html.H2(f"${max_rev:.2f}", className="text-primary")
                ])
            ], className="text-center mb-3"), width=6),
        ]),
        dcc.Graph(figure=fig)
    ])
