
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from app.data_manager import load_data

dash.register_page(__name__)

df = load_data()

# Inventory Mockup (Aggregate stock from latest entries per product)
# Since our data is transactional, we'll take the 'stock_quantity' from the most recent transaction for each product
latest_stock = df.sort_values('purchase_date').groupby('product_id').last().reset_index()
inventory_view = latest_stock[['product_id', 'brand', 'category', 'stock_quantity', 'current_price']].head(50)

# Add Status
def get_status(q):
    if q < 10: return 'Low Stock'
    if q > 40: return 'Overstocked'
    return 'Healthy'

inventory_view['Status'] = inventory_view['stock_quantity'].apply(get_status)

layout = dbc.Container([
    html.H2("Inventory Management", className="my-4"),
    
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Total Items in Stock"),
                html.H2(f"{inventory_view['stock_quantity'].sum()}", className="text-primary")
            ])
        ], className="text-center"), md=4),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Low Stock Alerts"),
                html.H2(f"{sum(inventory_view['Status']=='Low Stock')}", className="text-danger")
            ])
        ], className="text-center"), md=4),
    ], className="mb-4"),
    
    dash_table.DataTable(
        data=inventory_view.to_dict('records'),
        columns=[{"name": i, "id": i} for i in inventory_view.columns],
        page_size=15,
        style_cell={'textAlign': 'left'},
        style_data_conditional=[
            {
                'if': {'filter_query': '{Status} = "Low Stock"'},
                'backgroundColor': '#ffcccc',
                'color': 'red'
            },
            {
                'if': {'filter_query': '{Status} = "Overstocked"'},
                'backgroundColor': '#fff5cc',
                'color': 'orange'
            }
        ]
    )
], fluid=True)
