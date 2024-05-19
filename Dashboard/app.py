from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
from layout import create_layout
from dataFetch import fetch_years  # Import any other fetch functions as needed


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

years_options = fetch_years()
app.layout = create_layout(years_options)

if __name__ == '__main__':
    app.run_server(debug=True)

