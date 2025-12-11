import dash
from dash import dcc, html, Input, Output, State, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.data_manager import generate_synthetic_data
from app.model import PriceOptimModel

# Initialize App
app = dash.Dash(__name__, title="Price Optimization Engine")
server = app.server  # Expose for Gunicorn

# Load Initial Data
df = generate_synthetic_data(n_samples=2000)
products = df['Product'].unique()

# Pre-train models for efficiency (in prod, load from disk)
models = {}
for p in products:
    m = PriceOptimModel(p)
    m.train(df)
    models[p] = m

# Layout
app.layout = html.Div([
    html.Div([
        html.H1("Price Optimization Engine", style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.P("Simulate price changes and analyze impact on demand and profitability.", 
               style={'textAlign': 'center', 'color': '#7f8c8d'}),
    ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'marginBottom': '20px'}),

    html.Div([
        # Sidebar or Top Control Panel
        html.Div([
            html.Label("Select Product:"),
            dcc.Dropdown(
                id='product-dropdown',
                options=[{'label': p, 'value': p} for p in products],
                value=products[0],
                clearable=False
            ),
            html.Br(),
            html.Div(id='product-stats-card')
        ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),
        
        # Main Visualization Area
        html.Div([
            dcc.Graph(id='historical-graph'),
        ], style={'width': '70%', 'display': 'inline-block', 'padding': '10px'})
    ]),

    html.Hr(),

    html.Div([
        html.H3("Scenario Simulation"),
        html.Div([
            html.Label("Adjust Price Scenario (Multi-Price Analysis):"),
            dcc.Slider(
                id='price-range-slider',
                min=0, max=200, step=5,
                value=100,
                marks={i: str(i) for i in range(0, 201, 20)},
            ),
            html.P("Adjust the center point. The simulation runs +/- 20% around this price.", style={'fontSize': '12px'})
        ], style={'width': '80%', 'margin': 'auto'}),
        
        html.Div([
            dcc.Graph(id='simulation-graph')
        ], style={'marginTop': '20px'})
    ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderRadius': '5px', 'margin': '20px'})
])

# Callbacks
@callback(
    [Output('historical-graph', 'figure'),
     Output('product-stats-card', 'children'),
     Output('price-range-slider', 'value'),
     Output('price-range-slider', 'min'),
     Output('price-range-slider', 'max')],
    [Input('product-dropdown', 'value')]
)
def update_product_view(selected_product):
    prod_df = df[df['Product'] == selected_product]
    
    # Historical Time Series
    fig = px.line(prod_df, x='Date', y='Quantity', title=f'Historical Demand: {selected_product}')
    fig.update_layout(template='plotly_white')
    
    # Stats
    avg_price = prod_df['Price'].mean()
    elasticity = models[selected_product].metrics.get('elasticity', 0)
    
    stats = html.Div([
        html.P(f"Avg Price: ${avg_price:.2f}"),
        html.P(f"Avg Daily Sales: {prod_df['Quantity'].mean():.1f} units"),
        html.P(f"Est. Elasticity: {elasticity:.2f}", style={'fontWeight': 'bold', 
               'color': 'red' if elasticity < -1 else 'orange'})
    ], style={'border': '1px solid #ddd', 'padding': '10px', 'borderRadius': '5px'})
    
    # Update Slider range roughly around avg price
    base = int(avg_price)
    min_p = int(base * 0.5)
    max_p = int(base * 1.5)
    
    return fig, stats, base, min_p, max_p

@callback(
    Output('simulation-graph', 'figure'),
    [Input('product-dropdown', 'value'),
     Input('price-range-slider', 'value')]
)
def update_simulation(product, center_price):
    if not product or not center_price:
        return go.Figure()
    
    model = models[product]
    
    # Create a range around center_price
    prices = [p for p in range(int(center_price * 0.7), int(center_price * 1.3) + 1, 2)]
    if len(prices) < 2:
        prices = [center_price]
        
    sim_data = model.predict_scenario(prices)
    
    # Plot Revenue and Profit curves
    # Need to verify if 'Profit' is possible to calc in model or here.
    # Model returns Price, Predicted_Demand. 
    # We need cost. Let's approximate cost from the dataframe average for that product.
    avg_cost = df[df['Product'] == product]['Cost'].mean()
    
    sim_data['Revenue'] = sim_data['Price'] * sim_data['Predicted_Demand']
    sim_data['Profit'] = (sim_data['Price'] - avg_cost) * sim_data['Predicted_Demand']
    
    # Dual Axis graph
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=sim_data['Price'], y=sim_data['Revenue'], 
                             name='Projected Revenue', mode='lines', line=dict(color='blue')))
    
    fig.add_trace(go.Scatter(x=sim_data['Price'], y=sim_data['Profit'], 
                             name='Projected Profit', mode='lines', line=dict(color='green'), yaxis='y2'))
                             
    fig.update_layout(
        title=f"Projected Performance: {product} (Cost Base: ${avg_cost:.2f})",
        xaxis_title="Price ($)",
        yaxis_title="Revenue ($)",
        yaxis2=dict(title="Profit ($)", overlaying='y', side='right'),
        hovermode="x unified",
        template='plotly_white'
    )
    
    # Add a marker for current center
    fig.add_vline(x=center_price, line_dash="dash", annotation_text="Selected")
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
