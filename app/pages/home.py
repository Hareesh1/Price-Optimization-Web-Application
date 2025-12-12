
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from app.data_manager import load_data

dash.register_page(__name__, path='/')

df = load_data()

# Calculate Quick KPIs
total_rev = df['Revenue'].sum()
avg_margin = df['Margin'].mean()
return_rate = df['is_returned'].mean() * 100

layout = dbc.Container([
    # Hero Section
    dbc.Row([
        dbc.Col([
            html.H1("Retail Price Optimization & Analytics", className="display-3"),
            html.P(
                "Optimize prices, understand returns, and manage inventory using advanced machine learning.",
                className="lead"
            ),
            html.Hr(className="my-2"),
            html.P(
                "Explore the dashboard to unlock insights from your sales data."
            ),
            dbc.Button("Go to Analytics Dashboard", color="primary", href="/analytics", className="me-2"),
            dbc.Button("Try Price Optimization", color="secondary", outline=True, href="/price-optimizer"),
        ], width=12, className="py-5 text-center")
    ]),
    
    # KPI Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Total Revenue"),
            dbc.CardBody(html.H3(f"${total_rev:,.0f}", className="text-success"))
        ], className="text-center shadow-sm"), md=4),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader("Average Margin"),
            dbc.CardBody(html.H3(f"{avg_margin:.1f}%", className="text-info"))
        ], className="text-center shadow-sm"), md=4),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader("Return Rate"),
            dbc.CardBody(html.H3(f"{return_rate:.1f}%", className="text-danger"))
        ], className="text-center shadow-sm"), md=4),
    ], className="mb-5"),
    
    # Feature Grid
    dbc.Row([
        dbc.Col([
            html.H4("🛒 Sales Analytics"),
            html.P("Deep dive into sales trends by brand, category, and season.")
        ], md=4),
        dbc.Col([
            html.H4("💰 Price Optimization"),
            html.P("Simulate price changes to maximize revenue and profit.")
        ], md=4),
        dbc.Col([
            html.H4("📦 Return Intelligence"),
            html.P("Analyze return reasons and predict risky transactions.")
        ], md=4),
    ])
], fluid=True)
