from dash import dcc, html
import plotly.express as px
from dataFetch import fetch_weather_data, fetch_station_data
import pandas as pd
import plotly.graph_objects as go

def choropleth_map(selected_measurement, selected_year, selected_filter):
    # Fetch weather data for the selected year and filter
    weather_data = fetch_weather_data(selected_measurement, selected_year, selected_filter)

    # Fetch station data including name, country name, latitude, and longitude
    station_data = fetch_station_data()
    
    # Merge weather data and station data based on StationDWID
    merged_data = pd.merge(station_data, weather_data, on='StationDWID', how='inner')
    
    # Create custom scattermapbox trace
    trace = go.Scattermapbox(
        lat=merged_data["LATITUDE"],
        lon=merged_data["LONGITUDE"],
        mode="markers",
        marker=dict(
            size=10,  # Adjust the size of the points or squares
            color=merged_data["MeanValue"],  # Color based on the measurement value
            colorscale="Viridis",  # Choose a colorscale for coloring the points
            colorbar=dict(title=selected_measurement),  # Add a colorbar with measurement title
        ),
        hoverinfo="text",  # Show custom text on hover
        hovertext=merged_data.apply(
            lambda row: f"Station: {row['NAME']}<br>Country: {row['COUNTRY_NAME']}<br>{selected_measurement}: {row['MeanValue']}",
            axis=1,
        ),
    )
    
    # Create layout for the map
    layout = go.Layout(
        mapbox=dict(
            style="carto-positron",  # Change map style here
            zoom=3,
            center={"lat": 28.0339, "lon": 1.6596},  # Set center coordinates for North Africa
        ),
        margin=dict(l=0, r=0, t=0, b=0),  # Set margins to 0 on all sides
    )
    
    # Create figure with the custom trace and layout
    fig = go.Figure(data=[trace], layout=layout)
    
    return fig

def create_layout(years_options, measurements_options, seasons_options, quarters_options, semesters_options, months_options):
    # Define the initial values for year and measurement
    initial_year = 1920
    initial_measurement = 'PRCP'

    # Get the initial choropleth map figure
    initial_map_figure = choropleth_map(initial_measurement, initial_year, None)  # Pass None for the initial filter

    layout = html.Div([
        html.H1("Climatic Dashboard", style={'textAlign': 'center'}),

        html.Div([
            dcc.Dropdown(
                id='year-dropdown',
                options=years_options,
                value=initial_year,
                placeholder="Select a year",
                clearable=False,
                searchable=False,
                style={'width': '150px', 'marginRight': '20px'}
            ),
            dcc.Dropdown(
                id='season-dropdown',
                options=seasons_options,
                placeholder="Select a season",
                clearable=True,
                searchable=False,
                style={'width': '150px', 'marginRight': '20px'}
            ),
            dcc.Dropdown(
                id='quarter-dropdown',
                options=quarters_options,
                placeholder="Select a quarter",
                clearable=True,
                searchable=False,
                style={'width': '150px', 'marginRight': '20px'}
            ),
            dcc.Dropdown(
                id='semester-dropdown',
                options=semesters_options,
                placeholder="Select a semester",
                clearable=True,
                searchable=False,
                style={'width': '150px', 'marginRight': '20px'}
            ),
            dcc.Dropdown(
                id='month-dropdown',
                options=months_options,
                placeholder="Select a month",
                clearable=True,
                searchable=False,
                style={'width': '150px'}
            ),
            html.Div([
                dcc.RadioItems(
                    id='measurement-radio',
                    options=measurements_options,
                    value=initial_measurement,
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'}
                ),
                dcc.Graph(id='choropleth-map', figure=initial_map_figure, style={'width': '100%'})
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'})
    ])

    return layout
