from dash import dcc, html
import plotly.express as px
from dataFetch import fetch_weather_data, fetch_station_data
import pandas as pd
'''
def choropleth_map(selected_year, selected_measurement):
    # Fetch weather data for the selected year and measurement
    weather_data = fetch_weather_data(selected_measurement, selected_year)
    
    # Fetch station data including name, country name, latitude, and longitude
    station_data = fetch_station_data()
    
    # Merge weather data and station data based on StationDWID
    merged_data = pd.merge(station_data, weather_data, on='StationDWID', how='inner')
    
    # Create Choropleth map figure
    fig = px.scatter_mapbox(merged_data, lat="LATITUDE", lon="LONGITUDE", hover_name="NAME",
                            hover_data=["COUNTRY_NAME", "MeanValue"],
                            color="MeanValue", size="MeanValue",
                            color_continuous_scale=px.colors.sequential.Blues,
                            size_max=30, zoom=1, height=600)
    
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=1, mapbox_center={"lat": 31.7917, "lon": -7.0926})
    
    return fig
'''













import plotly.graph_objects as go
import pandas as pd

def choropleth_map(selected_year, selected_measurement):
    # Fetch weather data for the selected year and measurement
    weather_data = fetch_weather_data(selected_measurement, selected_year)
    
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
            colorscale="Blues",  # Choose a colorscale for coloring the points
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
            center={"lat": 28.0339, "lon": 1.6596},  # Set center coordinates for North Africa,
        ),
         margin=dict(l=0, r=0, t=0, b=0),  # Set margins to 0 on all sides
    )
    
    # Create figure with the custom trace and layout
    fig = go.Figure(data=[trace], layout=layout)
    
    return fig










def create_layout(years_options, measurements_options):
    # Define the initial values for year and measurement
    initial_year = 1920
    initial_measurement = 'PRCP'

    # Get the initial choropleth map figure
    initial_map_figure = choropleth_map(initial_year, initial_measurement)

    layout = html.Div([
        html.H1("Climatic Dashboard", style={'textAlign': 'center'}),
        html.Div([
            dcc.Dropdown(
                id='year-dropdown',
                options=years_options,
                value=initial_year,  # Default value for year dropdown
                clearable=False,  # Prevents the dropdown from being cleared
                searchable=False,  # Disables search functionality
                style={'width': '150px'}  # Set a fixed width for the dropdown
            ),
            html.Div(style={'width': '20px'}),  # Add space between dropdown and radio items
            dcc.RadioItems(
                id='measurement-radio',
                options=measurements_options,
                value=initial_measurement,  # Default value for measurement radio items
                labelStyle={'display': 'inline-block', 'margin-right': '20px'}
            ),
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}),  # Add marginBottom
        dcc.Graph(id='choropleth-map', figure=initial_map_figure)  # Initial state of the choropleth map
    ])

    return layout
