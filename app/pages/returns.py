
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from app.data_manager import load_data

dash.register_page(__name__)

df = load_data()

# Returns Analysis
return_reasons = df[df['is_returned']]['return_reason'].value_counts().reset_index()
return_reasons.columns = ['Reason', 'Count']

fig_reasons = px.pie(return_reasons, values='Count', names='Reason', title="Return Reasons Distribution", hole=0.4)
fig_reasons.update_layout(template='plotly_white')

# Returns by Category
cat_returns = df.groupby('category')['is_returned'].mean().reset_index()
fig_cat = px.bar(cat_returns, x='category', y='is_returned', title="Return Prob by Category", color='is_returned', color_continuous_scale='RdYlGn_r')
fig_cat.update_layout(template='plotly_white', yaxis_tickformat='.0%')

layout = dbc.Container([
    html.H2("Returns Intelligence", className="my-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_reasons), md=6),
        dbc.Col(dcc.Graph(figure=fig_cat), md=6),
    ]),
    
    html.Hr(),
    html.H4("Return Risk Predictor (Demo)"),
    dbc.Card([
        dbc.CardBody([
            html.P("Real-time risk scoring would go here using the classification model."),
            dbc.Progress(value=25, color="success", label="25% Risk", striped=True)
        ])
    ])
    
], fluid=True)
