import pymysql
import pandas as pd

# Function to connect to the database
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

# Function to fetch data from the database based on a given SQL query
def fetch_data(query):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            # Convert the fetched data to a Pandas DataFrame
            return pd.DataFrame(result)
    finally:
        connection.close()

########################################################################

# Function to fetch distinct years from the Date_Dim table
def fetch_years():
    query = "SELECT DISTINCT Year FROM Date_Dim ORDER BY Year ASC"
    years_df = fetch_data(query)  # Assuming fetch_data() returns a DataFrame
    # Convert the years data to list of dictionaries for dropdown options
    years_options = [{'label': year, 'value': year} for year in years_df['Year']]
    return years_options

# Function to fetch station data including name, country name, latitude, and longitude
def fetch_station_data():
    query = "SELECT StationDWID, NAME, COUNTRY_NAME, LATITUDE, LONGITUDE FROM station_dim"
    station_data = fetch_data(query)
    return station_data

# Function to fetch weather data for a selected measurement and year
def fetch_weather_data(selected_measurement, selected_year):
    query = f"""
    SELECT wf.StationDWID, AVG(wf.{selected_measurement}) AS MeanValue
    FROM weather_fact wf
    JOIN Date_Dim dd ON wf.DateDWID = dd.DateDWID
    WHERE dd.Year = {selected_year}
    GROUP BY wf.StationDWID
    """
    weather_data = fetch_data(query)
    return weather_data
