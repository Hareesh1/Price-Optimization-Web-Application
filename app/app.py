
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Initialize App with Multi-Page support and specialized Theme
app = dash.Dash(
    __name__, 
    use_pages=True, 
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True
)
server = app.server

# Standard Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Analytics", href="/analytics")),
        dbc.NavItem(dbc.NavLink("Price Optimizer", href="/price-optimizer")),
        dbc.NavItem(dbc.NavLink("Returns", href="/returns")),
        dbc.NavItem(dbc.NavLink("Inventory", href="/inventory")),
        dbc.NavItem(dbc.NavLink("Dataset", href="/dataset")),
    ],
    brand="RetailAI Analytics",
    brand_href="/",
    color="primary",
    dark=True,
    fluid=True,
    className="mb-4"
)

app.layout = html.Div([
    navbar,
    dash.page_container,
    # Footer
    html.Footer("© 2025 Retail Analytics Demo", className="text-center mt-5 p-4 text-muted")
])

if __name__ == '__main__':
    app.run(debug=True)
