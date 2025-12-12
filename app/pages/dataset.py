
import dash
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from app.data_manager import load_data

dash.register_page(__name__)

df = load_data()

layout = dbc.Container([
    html.H2("Dataset Overview", className="my-4"),
    
    dbc.Alert(
        "This dataset contains synthetic retail transactions designed to mimic real-world fashion boutique operations.",
        color="info"
    ),
    
    html.H4("First 100 Rows"),
    dash_table.DataTable(
        data=df.head(100).to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    ),
    
    html.Br(),
    html.H4("Data Dictionary"),
    dbc.Table.from_dataframe(pd.DataFrame({
        "Column": ["product_id", "category", "brand", "season", "original_price", "current_price", "is_returned"],
        "Description": [
            "Unique identifier", 
            "Apparel category (Dresses, Tops, etc.)",
            "Manufacturer brand",
            "Intended Season",
            "MSRP / Base Price",
            "Final Transaction Price",
            "True if item was returned"
        ]
    }), striped=True, bordered=True, hover=True),
    
    dbc.Button("Download Full CSV", id="btn-download", color="success", className="mt-3"),
    dcc.Download(id="download-dataframe-csv"),

], fluid=True)

# Note: Download callback would go here or in a separate callbacks file if needed. 
# For simplicity with Dash Pages, we can define callback here.
from dash import callback, Output, Input
@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, "retail_data.csv")
