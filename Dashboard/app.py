from dash.dependencies import Input, Output
from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_layout
from dataFetch import fetch_years
from layout import choropleth_map 




app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

years_options = fetch_years()

measurements_options = [
    {'label': 'PRCP', 'value': 'PRCP'},
    {'label': 'SNOW', 'value': 'SNOW'},
    {'label': 'SNWD', 'value': 'SNWD'},
    {'label': 'TAVG', 'value': 'TAVG'},
    {'label': 'TMIN', 'value': 'TMIN'},
    {'label': 'TMAX', 'value': 'TMAX'},
    {'label': 'PGTM', 'value': 'PGTM'},
    {'label': 'WSFG', 'value': 'WSFG'},
    {'label': 'WDFG', 'value': 'WDFG'}
]

# Register the callback
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('measurement-radio', 'value')]
)
def update_map(selected_year, selected_measurement):
    return choropleth_map(selected_year, selected_measurement)

# Set the app layout using the create_layout function
app.layout = create_layout(years_options, measurements_options)

if __name__ == '__main__':
    app.run_server(debug=True)

