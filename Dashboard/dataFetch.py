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

# Function to fetch distinct seasons from a Seasons table
def fetch_seasons(selected_year):
    query = f"""
        SELECT DISTINCT Season 
        FROM Date_Dim 
        WHERE Year = {selected_year} 
    """
    seasons_df = fetch_data(query)
    seasons_options = [{'label': season, 'value': season} for season in seasons_df['Season']]
    return seasons_options


# Function to fetch distinct months from Date_Dim table
def fetch_months(selected_year):
    query = f"""
         SELECT DISTINCT Month_Name 
         FROM Date_Dim
         WHERE Year = {selected_year} 
    """
    months_df = fetch_data(query)  # Assuming fetch_data() returns a DataFrame
    months_options = [{'label': month, 'value': month} for month in months_df['Month_Name']]
    return months_options




# Function to fetch distinct quarters for a specific year from Date_Dim table
def fetch_quarters(selected_year):
    query = f"""
        SELECT DISTINCT Year_And_Quarter 
        FROM Date_Dim 
        WHERE Year = {selected_year} 
        ORDER BY Year_And_Quarter ASC
    """
    quarters_df = fetch_data(query)  # Assuming fetch_data() returns a DataFrame
    # Convert the quarters data to a list of dictionaries for dropdown options
    quarters_options = [{'label': quarter, 'value': quarter} for quarter in quarters_df['Year_And_Quarter']]
    return quarters_options


# Function to fetch distinct semesters for a specific year from Date_Dim table
def fetch_semesters(selected_year):
    query = f"""
        SELECT DISTINCT Year_And_Semester 
        FROM Date_Dim 
        WHERE Year = {selected_year} 
        ORDER BY Year_And_Semester ASC
    """
    semesters_df = fetch_data(query)  # Assuming fetch_data() returns a DataFrame
    # Convert the semesters data to a list of dictionaries for dropdown options
    semesters_options = [{'label': semester, 'value': semester} for semester in semesters_df['Year_And_Semester']]
    return semesters_options


# Function to fetch station data including name, country name, latitude, and longitude
def fetch_station_data():
    query = "SELECT StationDWID, NAME, COUNTRY_NAME, LATITUDE, LONGITUDE FROM station_dim"
    station_data = fetch_data(query)
    return station_data



# Function to fetch weather data for a selected measurement, year, and filter

def fetch_weather_data(selected_measurement, selected_year, selected_filter):
    # Start building the query
    query = f"""
        SELECT wf.StationDWID, AVG(wf.{selected_measurement}) AS MeanValue
        FROM weather_fact wf
        JOIN Date_Dim dd ON wf.DateDWID = dd.DateDWID
        WHERE dd.Year = {selected_year}
    """

    # Add the filter based on the specific type
    if selected_filter:
        if selected_filter in ["Spring", "Summer", "Fall", "Winter"]:  # Season filter
            query += f" AND dd.Season = '{selected_filter}'"
        elif '-S' in selected_filter:  # Semester filter, e.g., "YYYY-Sn"
            query += f" AND dd.Year_And_Semester = '{selected_filter}'"
        elif 'Q' in selected_filter:  # Quarter filter, e.g., "YYYYQn"
            query += f" AND dd.Year_And_Quarter = '{selected_filter}'"
        else:  # Month filter
            query += f" AND dd.Month_Name = '{selected_filter}'"
    
    # Finish the query
    query += " GROUP BY wf.StationDWID"

    # Fetch the data
    weather_data = fetch_data(query)
    return weather_data
