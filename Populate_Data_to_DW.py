import pymysql
import pandas as pd
import datetime


# Fonction pour convertir la date compléte de format 'YYYY-MM-DD' à 'YYYYMMDD'
def get_id_date(fulldate):
    return datetime.datetime.strptime(fulldate, '%Y-%m-%d').strftime('%Y%m%d')
  
    
  
# Fonction qui combinne la date et le code du sation 
# pour génénrer un dateid unique
def generate_DateDWID(fulldate, sationcode):
    date_part = get_id_date(fulldate)
    return f"{date_part}{sationcode}"  



# Fonction pour peupler la table Date_Dim

def populate_Date_Dim(cursor, csvpath):
    
    # Lire le fichier CSV en utilisant uniquement les colonnes nécessaires
    Date_Dim = pd.read_csv(csvpath, usecols=['Full_date', 'Day_Name', 'WeekendFlag',
                                             'Month_Name', 'Month', 
                                             'quarter','semester',
                                             'Season', 'year'])
    
    
   
                                                        
    for _, row in Date_Dim.iterrows():
        # Convertir la date compléte pour quelle s'adapte
        # avec le type de l'attribut "DateDWID" de la table 'Date_Dim'
        FullDate = get_id_date(row['Full_date'])
        
        # Utilise la fonction generate_DateDWID pour génerer la clé primaire de la table 'Date_Dim'
        DATEID = generate_DateDWID(row['Full_date'],row['STATION'])
        
        query_insert = "INSERT INTO Date_Dim ( DateDWID, Full_Date, Day_Name, WeekendFlag," \
                                             " Month_Name, Month_Number,"\
                                             " Year_And_Quarter, Year_And_Semester, " \
                                             " Season, Year)" \
                                     "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                                   
        values = ( DATEID, FullDate, row['Day_Name'], row['WeekendFlag'],
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
def populate_Weather_Fact(cursor, csv_path): 
    # Lire le fichier CSV en utilisant uniquement les colonnes nécessaires
    FactWeather = pd.read_csv(csv_path, usecols = ['STATION','Full_date','PRCP', 'SNOW', 'SNWD',
                                                   'TAVG', 'TMIN', 'TMAX',
                                                   'PGTM', 'WSFG','WDFG'])
    
    # Remplacer les valeurs NaN par 'N/A' dans le DataFrame FactWeather
    FactWeather.fillna('N/A', inplace=True)
        
    
    for _, row in FactWeather.iterrows():
        DATEID = generate_DateDWID(row['Full_date'],row['STATION'])


        query_insert = "INSERT INTO Weather_Fact ( DateDWID , PRCP, SNOW , SNWD ,TAVG, TMIN, TMAX, PGTM, WSFG , WDFG ) "\
                                         "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        
        values = (DATEID, row['PRCP'], row['SNOW'], row['SNWD'],
                  row['TAVG'], row['TMIN'], row['TMAX'],
                  row['PGTM'], row['WSFG'] , row['WDFG'])
        
        
        cursor.execute(query_insert, values)
        
        
        
        
# Connecter à la BDD 'WeatherDataWarehouse'
connection = pymysql.connect(host='localhost',
                               user='root',
                               password='',
                               database='WeatherDataWarehouse',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

print("Start populating 'Date_Dim' table" )
populate_Date_Dim(cursor,"climatic_dataSet.csv")
print("'Date_Dim' populated")

print("\nStart populating 'Station_Dim' table" )
populate_Station_Dim(cursor,"climatic_dataSet.csv")
print("'Station_Dim' populated")

print("\nStart populating 'Weather_Fact' table" )
populate_Weather_Fact(cursor,"climatic_dataSet.csv")
print("'Weather_Fact' populated")



# Fermer la connexion
cursor.close()
connection.commit()
connection.close()