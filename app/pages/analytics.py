
import dash
from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
from app.data_manager import load_data, get_filter_options

dash.register_page(__name__)

df = load_data()
options = get_filter_options(df)

layout = dbc.Container([
    dbc.Row([
        # Sidebar
        dbc.Col([
            html.H4("Filters", className="mt-4"),
            html.Label("Brand"),
            dcc.Dropdown(
                id='filter-brand',
                options=[{'label': i, 'value': i} for i in options['brands']],
                multi=True,
                placeholder="All Brands"
            ),
            html.Br(),
            html.Label("Category"),
            dcc.Dropdown(
                id='filter-category',
                options=[{'label': i, 'value': i} for i in options['categories']],
                multi=True,
                placeholder="All Categories"
            ),
            html.Br(),
            html.Label("Season"),
            dcc.Checklist(
                id='filter-season',
                options=[{'label': i, 'value': i} for i in options['seasons']],
                value=options['seasons'],
                inline=False,
                inputStyle={"marginRight": "5px"}
            )
        ], md=3, className="bg-light p-4"),
        
        # Main Dashboard
        dbc.Col([
            html.H2("Sales Performance Analytics", className="my-4"),
            
            # Top Row Charts
            dbc.Row([
                dbc.Col(dcc.Graph(id='revenue-trend'), md=12),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='sales-by-brand'), md=6),
                dbc.Col(dcc.Graph(id='category-season-heatmap'), md=6),
            ], className="mt-4")
            
        ], md=9)
    ])
], fluid=True)

@callback(
    [Output('revenue-trend', 'figure'),
     Output('sales-by-brand', 'figure'),
     Output('category-season-heatmap', 'figure')],
    [Input('filter-brand', 'value'),
     Input('filter-category', 'value'),
     Input('filter-season', 'value')]
)
def update_analytics(brands, categories, seasons):
    dff = df.copy()
    
    # Apply Filters
    if brands:
        dff = dff[dff['brand'].isin(brands)]
    if categories:
        dff = dff[dff['category'].isin(categories)]
    if seasons:
        dff = dff[dff['season'].isin(seasons)]
        
    # 1. Revenue over Time
    # Aggregate by Month
    dff['Month'] = dff['purchase_date'].dt.to_period('M').astype(str)
    monthly_rev = dff.groupby('Month')['Revenue'].sum().reset_index()
    fig1 = px.line(monthly_rev, x='Month', y='Revenue', title="Revenue Trend (Monthly)", markers=True)
    fig1.update_layout(template='plotly_white')
    
    # 2. Sales by Brand
    brand_sales = dff.groupby('brand')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)
    fig2 = px.bar(brand_sales, x='Revenue', y='brand', orientation='h', title="Revenue by Brand")
    fig2.update_layout(template='plotly_white')
    
    # 3. Category vs Season Heatmap (Pivot)
    heatmap_data = dff.pivot_table(index='category', columns='season', values='Revenue', aggfunc='sum', fill_value=0)
    fig3 = px.imshow(heatmap_data, title="Revenue Heatmap: Category vs Season", text_auto='.2s')
    fig3.update_layout(template='plotly_white')
    
    return fig1, fig2, fig3
