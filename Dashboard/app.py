from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from layout import create_layout, choropleth_map, line_plot
from dataFetch import fetch_years, fetch_seasons, fetch_quarters, fetch_semesters, fetch_months
import dash

app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

# Fetch options for years
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

# Register the callback to update quarters and semesters options based on the selected year
@app.callback(
    [
        Output('season-dropdown', 'options'),
        Output('quarter-dropdown', 'options'),
        Output('semester-dropdown', 'options'),
        Output('month-dropdown', 'options')
    ],
    [
        Input('year-dropdown', 'value')
    ]
)
def update_quarters_semesters(selected_year):
    seasons_options = fetch_seasons(selected_year) 
    quarters_options = fetch_quarters(selected_year)  # Fetch quarters options for the selected year
    semesters_options = fetch_semesters(selected_year)  # Fetch semesters options for the selected year
    months_options = fetch_months(selected_year)  
    return seasons_options, quarters_options, semesters_options, months_options




# Register the callback to update the map
@app.callback(
    Output('choropleth-map', 'figure'),
    [
        Input('year-dropdown', 'value'),
        Input('season-dropdown', 'value'),
        Input('quarter-dropdown', 'value'),
        Input('semester-dropdown', 'value'),
        Input('month-dropdown', 'value'),
        Input('measurement-radio', 'value')
    ]
)
def update_map(selected_year, selected_season, selected_quarter, selected_semester, selected_month, selected_measurement):
    selected_filter = selected_season or selected_quarter or selected_semester or selected_month
    return choropleth_map(selected_measurement, selected_year, selected_filter)





@app.callback(
    Output('line-plot', 'figure'),
    [Input('measurement-radio', 'value')]
)
def update_line_plot(selected_measurement):
    return line_plot(selected_measurement)



# Register the callback to clear other dropdowns
@app.callback(
    [
        Output('season-dropdown', 'value'),
        Output('quarter-dropdown', 'value'),
        Output('semester-dropdown', 'value'),
        Output('month-dropdown', 'value')
    ],
    [
        Input('season-dropdown', 'value'),
        Input('quarter-dropdown', 'value'),
        Input('semester-dropdown', 'value'),
        Input('month-dropdown', 'value')
    ]
)
def clear_other_dropdowns(season, quarter, semester, month):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'season-dropdown' and season:
        return season, None, None, None
    elif trigger_id == 'quarter-dropdown' and quarter:
        return None, quarter, None, None
    elif trigger_id == 'semester-dropdown' and semester:
        return None, None, semester, None
    elif trigger_id == 'month-dropdown' and month:
        return None, None, None, month
    else:
        return None, None, None, None

# Set the app layout using the create_layout function
app.layout = create_layout(years_options, measurements_options, [], [], [], [])

if __name__ == '__main__':
    app.run_server(debug=True)


