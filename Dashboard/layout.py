from dash import dcc, html
import plotly.express as px
from dataFetch import fetch_weather_data, fetch_station_data, fetch_weather_data_forGraph
import pandas as pd
import plotly.graph_objects as go

# Fonction pour créer une carte choroplèthe basée sur la mesure et l'année sélectionnées
def choropleth_map(selected_measurement, selected_year, selected_filter):
    # Récupérer les données météorologiques pour l'année et le filtre sélectionnés
    weather_data = fetch_weather_data(selected_measurement, selected_year, selected_filter)

    # Récupérer les données des stations
    station_data = fetch_station_data()
    
    # Fusionner les données météorologiques et les données des stations
    merged_data = pd.merge(station_data, weather_data, on='StationDWID', how='inner')
    
    # Créer une trace de Scattermapbox personnalisée
    trace = go.Scattermapbox(
        lat=merged_data["LATITUDE"],
        lon=merged_data["LONGITUDE"],
        mode="markers",
        marker=dict(
            size=10,  # Ajuster la taille des points
            color=merged_data["MeanValue"],  # Couleur basée sur la valeur de la mesure
            colorscale="Viridis",  # Choisir une échelle de couleurs
            colorbar=dict(title=selected_measurement),  # Ajouter une barre de couleurs avec le titre de la mesure
        ),
        hoverinfo="text",  # Afficher le texte personnalisé au survol
        hovertext=merged_data.apply(
            lambda row: f"Station: {row['NAME']}<br>Country: {row['COUNTRY_NAME']}<br>{selected_measurement}: {row['MeanValue']}",
            axis=1,
        ),
    )
    
    # Créer la mise en page pour la carte
    layout = go.Layout(
        mapbox=dict(
            style="carto-positron",  # Changer le style de la carte ici
            zoom=3,
            center={"lat": 28.0339, "lon": 1.6596},  # Définir les coordonnées centrales pour l'Afrique du Nord
        ),
        margin=dict(l=0, r=0, t=0, b=0),  # Définir les marges à 0 de tous les côtés
    )
    
    # Créer la figure avec la trace personnalisée et la mise en page
    fig = go.Figure(data=[trace], layout=layout)
    
    return fig






################################################################

# Fonction pour créer un graphique en ligne basé sur la mesure sélectionnée
def line_plot(selected_measurement):
    # Récupérer les données météorologiques pour le graphique
    weather_data = fetch_weather_data_forGraph(selected_measurement)

    # Créer le graphique en ligne
    fig = px.line(
        weather_data, 
        x='Decade', 
        y='MeanValue', 
        color='COUNTRY_NAME',
        markers=True,
        title=f'{selected_measurement} Over Decades by Country'
    )
    
    # Mettre à jour la mise en page du graphique
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

# Fonction pour créer la mise en page de l'application
def create_layout(years_options, measurements_options, seasons_options, quarters_options, semesters_options, months_options):
    # Définir les valeurs initiales pour l'année et la mesure
    initial_year = 1920
    initial_measurement = 'PRCP'

    # Obtenir la figure initiale de la carte choroplèthe
    initial_map_figure = choropleth_map(initial_measurement, initial_year, None)  # Passer None pour le filtre initial

    # Obtenir la figure initiale du graphique en ligne
    initial_line_figure = line_plot(initial_measurement)

    layout = html.Div([
        html.Div([
            html.H1("Maghreb Climate Dashboard : Historical Data (1920-2022)", style={'textAlign': 'center'}),
        ], style={'margin-bottom': '50px'}),

        html.Div([
            html.Div([
                html.H3("Filters", style={'margin-bottom': '10px'}),  # Ajouter du texte au-dessus des listes déroulantes
                
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
                html.Label("Choose a climatic measurment ", style={'margin-bottom': '5px', 'margin-top': '40px'}),
                dcc.RadioItems(
                    id='measurement-radio',
                    options=measurements_options,
                    value=initial_measurement,
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'}
                ),
                dcc.Graph(id='choropleth-map', figure=initial_map_figure, style={'width': '100%', 'height': '380px', 'margin-top': '20px'}),
                html.H4("--Interactive Map of Maghreb Climate Data--", style={'textAlign': 'center', 'margin-top': '10px'}) 
            ], style={'flex': '2', 'margin-left': '20px'})
        ], style={'display': 'flex', 'align-items': 'flex-start', 'margin-bottom': '20px', 'justify-content': 'center'}),

        # Ajouter le graphique en ligne en dessous de la carte et des listes déroulantes
        html.Div([
            dcc.Graph(id='line-plot', figure=initial_line_figure, style={'width': '100%', 'height': '100%', 'margin-top': '100px'}),
            html.H4("--Comparative Climatic Plotline : Algeria VS Morocco VS Tunisia--", style={'textAlign': 'center', 'margin-top': '10px', 'margin-bottom': '50px'}), 
        ])
    ], style={'max-width': '1200px', 'margin': '0 auto'})

    return layout
