import pymysql
import pandas as pd

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

def fetch_data(query):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return pd.DataFrame(result)
    finally:
        connection.close()


########################################################################


def fetch_years():
    query = "SELECT DISTINCT Year FROM Date_Dim ORDER BY Year ASC"
    years_df = fetch_data(query)  # Assuming fetch_data() returns a DataFrame
    # Convert the years data to list of dictionaries for dropdown options
    years_options = [{'label': year, 'value': year} for year in years_df['Year']]
    return years_options
