from dash import dcc, html
import plotly.express as px
from dataFetch import fetch_weather_data, fetch_station_data , fetch_weather_data_forGraph
import pandas as pd
import plotly.graph_objects as go
from dataFetch import *

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



################################################################


def line_plot(selected_measurement):
    weather_data = fetch_weather_data_forGraph(selected_measurement)

    fig = px.line(
        weather_data, 
        x='Decade', 
        y='MeanValue', 
        color='COUNTRY_NAME',
        markers=True,
        title=f'{selected_measurement} Over Decades by Country'
    )
    
    fig.update_layout(
        xaxis_title='Decade',
        yaxis_title=selected_measurement,
        legend_title_text='Country',
        xaxis=dict(
            tickmode='linear',
            dtick=10
        )
    )
    
    return fig





################################################################



def create_layout(years_options, measurements_options, seasons_options, quarters_options, semesters_options, months_options):
    # Define the initial values for year and measurement
    initial_year = 1920
    initial_measurement = 'PRCP'

    # Get the initial choropleth map figure
    initial_map_figure = choropleth_map(initial_measurement, initial_year, None)  # Pass None for the initial filter

     # Get the initial time series graph figure
    #initial_time_series_figure = time_series_graph(initial_measurement, initial_year, None)  # Pass None for the initial filter

    initial_line_figure = line_plot(initial_measurement)

    layout = html.Div([
        html.Div([
            html.H1("Maghreb Climate Dashboard : Historical Data (1920-2022)", style={'textAlign': 'center'}),
        ], style={'margin-bottom': '50px'}),

        html.Div([
            html.Div([
                html.H3("Filters", style={'margin-bottom': '10px'}),  # Add text above dropdowns
                
                html.Label("Select Year", style={'margin-bottom': '5px'}),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=years_options,
                    value=initial_year,
                    placeholder="Select a year",
                    clearable=False,
                    searchable=False,
                    style={'width': '200px', 'margin-bottom': '60px'}
                ),

                html.Label("Select Additional Filter", style={'margin-bottom': '5px'}),
                dcc.Dropdown(
                    id='season-dropdown',
                    options=seasons_options,
                    placeholder="Select a season",
                    clearable=True,
                    searchable=False,
                    style={'width': '200px', 'margin-bottom': '50px'}
                ),
                dcc.Dropdown(
                    id='quarter-dropdown',
                    options=quarters_options,
                    placeholder="Select a quarter",
                    clearable=True,
                    searchable=False,
                    style={'width': '200px', 'margin-bottom': '50px'}
                ),
                dcc.Dropdown(
                    id='semester-dropdown',
                    options=semesters_options,
                    placeholder="Select a semester",
                    clearable=True,
                    searchable=False,
                    style={'width': '200px', 'margin-bottom': '50px'}
                ),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=months_options,
                    placeholder="Select a month",
                    clearable=True,
                    searchable=False,
                    style={'width': '200px', 'margin-bottom': '50px'}
                ),
            ], style={'flex': '1', 'margin-right': '20px', 'max-width': '220px'}),

            html.Div([
                html.Label("Choose a climatic measurment ", style={'margin-bottom': '5px' , 'margin-top': '40px'}),
                dcc.RadioItems(
                    id='measurement-radio',
                    options=measurements_options,
                    value=initial_measurement,
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'}
                ),
                dcc.Graph(id='choropleth-map', figure=initial_map_figure, style={'width': '100%','height': '380px', 'margin-top': '20px'}),
                html.H4("--Interactive Map of Maghreb Climate Data--", style={'textAlign': 'center', 'margin-top': '10px'}) 
            ], style={'flex': '2', 'margin-left': '20px'})
        ], style={'display': 'flex', 'align-items': 'flex-start', 'margin-bottom': '20px', 'justify-content': 'center'}),

        # Add the time series graph below the map and dropdowns
        html.Div([
            dcc.Graph(id='line-plot', figure=initial_line_figure, style={'width': '100%','height': '100%', 'margin-top': '100px'}),
            html.H4("--Comparative Climatic Plotline : Algeria VS Morocco VS Tunisia--", style={'textAlign': 'center', 'margin-top': '10px', 'margin-bottom': '50px'}), 
        ])
    ],style={'max-width': '1200px', 'margin': '0 auto'})

    return layout
