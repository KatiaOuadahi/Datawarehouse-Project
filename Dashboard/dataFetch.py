import pymysql
import pandas as pd

# Fonction pour se connecter à la base de données
def connect_to_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='WeatherDataWarehouse',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Fonction pour récupérer les données de la base de données en fonction d'une requête SQL donnée
def fetch_data(query):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            # Convertir les données récupérées en DataFrame Pandas
            return pd.DataFrame(result)
    finally:
        connection.close()




########################################################################




# Fonction pour récupérer les années distinctes de la table Date_Dim
def fetch_years():
    query = "SELECT DISTINCT Year FROM Date_Dim ORDER BY Year ASC"
    years_df = fetch_data(query)
    # Convertir les années en liste de dictionnaires pour les options de la liste déroulante
    years_options = [{'label': year, 'value': year} for year in years_df['Year']]
    return years_options



# Fonction pour récupérer les saisons distinctes pour une année donnée
def fetch_seasons(selected_year):
    query = f"""
        SELECT DISTINCT Season 
        FROM Date_Dim 
        WHERE Year = {selected_year}
    """
    seasons_df = fetch_data(query)
    seasons_options = [{'label': season, 'value': season} for season in seasons_df['Season']]
    return seasons_options



# Fonction pour récupérer les mois distincts pour une année donnée
def fetch_months(selected_year):
    query = f"""
         SELECT DISTINCT Month_Name 
         FROM Date_Dim
         WHERE Year = {selected_year} 
    """
    months_df = fetch_data(query)
    months_options = [{'label': month, 'value': month} for month in months_df['Month_Name']]
    return months_options




# Fonction pour récupérer les trimestres distincts pour une année donnée
def fetch_quarters(selected_year):
    query = f"""
        SELECT DISTINCT Year_And_Quarter 
        FROM Date_Dim 
        WHERE Year = {selected_year} 
        ORDER BY Year_And_Quarter ASC
    """
    quarters_df = fetch_data(query)
    quarters_options = [{'label': quarter, 'value': quarter} for quarter in quarters_df['Year_And_Quarter']]
    return quarters_options




# Fonction pour récupérer les semestres distincts pour une année donnée
def fetch_semesters(selected_year):
    query = f"""
        SELECT DISTINCT Year_And_Semester 
        FROM Date_Dim 
        WHERE Year = {selected_year} 
        ORDER BY Year_And_Semester ASC
    """
    semesters_df = fetch_data(query)
    semesters_options = [{'label': semester, 'value': semester} for semester in semesters_df['Year_And_Semester']]
    return semesters_options




# Fonction pour récupérer les données des stations incluant le nom, le nom du pays, la latitude et la longitude
def fetch_station_data():
    query = "SELECT StationDWID, NAME, COUNTRY_NAME, LATITUDE, LONGITUDE FROM station_dim"
    station_data = fetch_data(query)
    return station_data



# Fonction pour récupérer les données météorologiques pour une mesure, une année et un filtre sélectionnés
def fetch_weather_data(selected_measurement, selected_year, selected_filter):
    # Construire la requête SQL
    query = f"""
        SELECT wf.StationDWID, AVG(wf.{selected_measurement}) AS MeanValue
        FROM weather_fact wf
        JOIN Date_Dim dd ON wf.DateDWID = dd.DateDWID
        WHERE dd.Year = {selected_year}
    """
    # Ajouter le filtre en fonction du type spécifique
    if selected_filter:
        if selected_filter in ["Spring", "Summer", "Fall", "Winter"]:  # Filtre saison
            query += f" AND dd.Season = '{selected_filter}'"
        elif '-S' in selected_filter:  # Filtre semestre, ex. "YYYY-Sn"
            query += f" AND dd.Year_And_Semester = '{selected_filter}'"
        elif 'Q' in selected_filter:  # Filtre trimestre, ex. "YYYYQn"
            query += f" AND dd.Year_And_Quarter = '{selected_filter}'"
        else:  # Filtre mois
            query += f" AND dd.Month_Name = '{selected_filter}'"
    
    query += " GROUP BY wf.StationDWID"

    weather_data = fetch_data(query)
    return weather_data




# Fonction pour récupérer les données météorologiques pour le graphique en fonction d'une mesure sélectionnée
def fetch_weather_data_forGraph(selected_measurement):
    query = f"""
        SELECT FLOOR(dd.Year / 10) * 10 AS Decade, 
               AVG(wf.{selected_measurement}) AS MeanValue, 
               st.COUNTRY_NAME
        FROM weather_fact wf
        JOIN Date_Dim dd ON wf.DateDWID = dd.DateDWID
        JOIN station_dim st ON wf.StationDWID = st.StationDWID
        WHERE dd.Year BETWEEN 1920 AND 2022
        GROUP BY Decade, st.COUNTRY_NAME
        ORDER BY Decade
    """
    weather_data = fetch_data(query)
    return weather_data
