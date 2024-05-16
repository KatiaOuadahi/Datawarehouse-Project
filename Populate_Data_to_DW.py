import pymysql
import pandas as pd
import datetime


# Convertir la date complaite de format 'YYYY-MM-DD' à 'YYYYMMDD'
def get_id_date(fulldate):
    return datetime.datetime.strptime(fulldate, '%Y-%m-%d').strftime('%Y%m%d')
  
    
  
# Fonction pour peupler la table Date_Dim
def populate_Date_Dim(cursor, csvpath):
    
    # Lire le fichier CSV en utilisant uniquement les colonnes nécessaires
    Date_Dim = pd.read_csv(csvpath, usecols=['Full_date', 'Day_Name', 'WeekendFlag',
                                             'Month_Name', 'Month', 
                                             'quarter','semester',
                                             'Season', 'year'])
    
    
   
                                                        
    for _, row in Date_Dim.iterrows():
        Date = get_id_date(row['Full_date']) 
        
        query_insert = "INSERT INTO Date_Dim ( Full_Date, Day_Name, WeekendFlag," \
                                           " Month_Name, Month_Number,"\
                                           " Year_And_Quarter, Year_And_Semester, " \
                                           " Season, Year)" \
                                   "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                                   
        values = ( Date, row['Day_Name'], row['WeekendFlag'],
                   row['Month_Name'], row['Month'], row['quarter'],
                   row['semester'], row['Season'], row['year'])
                         
        cursor.execute(query_insert, values)
        



##############################################################################################

# Fonction pour peupler la table Station_Dim
def populate_Station_Dim(cursor, csv_path): 
    
    # Lire le fichier CSV en utilisant uniquement les colonnes nécessaires  
    Station_Dim = pd.read_csv(csv_path, usecols=['STATION' , 'NAME' , 'country_name' , 'LATITUDE' , 'LONGITUDE' , 'ELEVATION'])

    for _, row in Station_Dim.iterrows():
        query_insert = "INSERT INTO Station_Dim ( StationID , NAME , COUNTRY_NAME , LATITUDE , LONGITUDE , ELEVATION)"\
                                      "VALUES ( %s, %s, %s, %s, %s, %s ) "
        
        values = (row['STATION'], row['NAME'],
                  row['country_name'] ,row['LATITUDE'],
                  row['LONGITUDE'], row['ELEVATION'])
        
        cursor.execute(query_insert, values)
        


##########################################################################################

# Fonction pour peupler la table fact_Weather
def populate_Weather_fact(cursor, csv_path): 
    # Lire le fichier CSV en utilisant uniquement les colonnes nécessaires
    FactWeather = pd.read_csv(csv_path, usecols=['Full_date','PRCP', 'SNOW', 'SNWD',
                                                 'TAVG', 'TMIN', 'TMAX',
                                                 'PGTM', 'WSFG','WDFG'])
    
    # Remplacer les valeurs NaN par 'N/A' dans le DataFrame FactWeather
    FactWeather.fillna('N/A', inplace=True)
        
    
    for _, row in FactWeather.iterrows():
        # Convertir la date complète en format YYYYMMDD 
        # pour être inserer dans la colonne DateDWID
        Date = get_id_date(row['Full_date']) 

        query_insert = "INSERT INTO Weather_Fact ( DateDWID , PRCP, SNOW , SNWD ,TAVG, TMIN, TMAX, PGTM, WSFG , WDFG ) "\
                                       "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        
        values = (Date, row['PRCP'], row['SNOW'], row['SNWD'],
                  row['TAVG'], row['TMIN'], row['TMAX'],
                  row['PGTM'], row['WSFG'] , row['WDFG'])
        
        
        cursor.execute(query_insert, values)
        
        
        
        
# Connecte to the DataBase
connection = pymysql.connect(host='localhost',
                               user='root',
                               password='',
                               database='WeatherDataWarehouse',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

populate_Date_Dim(cursor,"climatic_dataSet.csv")
print("Date Dim populated")

populate_Station_Dim(cursor,"climatic_dataSet.csv")
print("Station Dim populated")


populate_Weather_fact(cursor,"climatic_dataSet.csv")
print("Weather Fact populated")



# Close the connection
cursor.close()
connection.commit()
connection.close()