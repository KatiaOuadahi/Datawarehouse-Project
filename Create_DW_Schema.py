import pymysql

# Fonction pour créer la base de données "Weather_DataWarehouse"
def Create_Weather_Datawarehouse(cursor):
    sql = "CREATE DATABASE IF NOT EXISTS WeatherDataWarehouse"
    cursor.execute(sql)
    
    
# Fonction pour créer une table dans la base de données 
def Create_Table(co_cursor, table_name, table_schema):
    try:
        co_cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        sql_drop = "DROP TABLE IF EXISTS " + table_name
        co_cursor.execute(sql_drop)
        sql_create = "CREATE TABLE " + table_name + "(" + table_schema + ")"
        co_cursor.execute(sql_create)
    except Exception as e:
        print("Error creating table:", e)
    finally:
        co_cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


# Se connecter à la base de données pour créer la BDD "Weather_DataWarehouse"
con = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

# Créer un curseur pour exécuter les requêtes SQL
cursor = con.cursor()  

# Appeler la fonction pour créer la BDD "Weather_DataWarehouse"
Create_Weather_Datawarehouse(cursor)
print("Weather_DataWarehouse Database was Created successfly")

# Fermer le curseur et valider les modifications dans la base de données
# Fermer la connexion à la base de données
cursor.close()
con.commit()
con.close()


############################################################################
# Se reconnecter à la BDD "Weather_DataWarehouse" 
# pour créer le schéma en étoile
connection = pymysql.connect(host='localhost',
                               user='root',
                               password='',
                               database='WeatherDataWarehouse',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()



Create_Table(cursor, "Station_Dim" ," StationDWID INT AUTO_INCREMENT, StationID VARCHAR(30) , NAME VARCHAR(50),"
                                    " COUNTRY_NAME CHAR(20), LATITUDE FLOAT, LONGITUDE FLOAT, ELEVATION FLOAT,"
                                    " PRIMARY KEY (StationDWID)")

print("Station_Dim Table was Created successfly")

###################################################

Create_Table(cursor, "Date_Dim" ," DateDWID VARCHAR(8) GENERATED ALWAYS AS (DATE_FORMAT(Full_Date,'%Y%m%d')) STORED,"
                                 " Full_Date DATE, Day_Name VARCHAR(10), WeekendFlag BOOL,"
                                 " Month_Name VARCHAR(15), Month_Number INT(2), Year_And_Semester VARCHAR(10),"
                                 " Year_And_Quarter VARCHAR(10), Season CHAR(10), Year YEAR,  "
                                 " PRIMARY KEY (DateDWID)")

print("Date_Dim Table was Created successfly")


##################################################

Create_Table(cursor, "Weather_Fact" ," StationDWID INT NOT NULL AUTO_INCREMENT , DateDWID VARCHAR(8) NOT NULL, PRCP VARCHAR(10) , SNOW VARCHAR(10) NULL,"
                                     " SNWD VARCHAR(10) NULL,TAVG VARCHAR(10) NULL, TMIN VARCHAR(10) NULL, TMAX VARCHAR(10) NULL,"
                                     " PGTM VARCHAR(10) NULL, WSFG VARCHAR(10) NULL, WDFG VARCHAR(10) NULL ,"
                                     " PRIMARY KEY (StationDWID, DateDWID),"
                                     " FOREIGN KEY (DateDWID) REFERENCES  Date_Dim(DateDWID),"
                                     " FOREIGN KEY (StationDWID) REFERENCES  Station_Dim(StationDWID)")

print("Weather_Fact Table was Created successfly")





cursor.close()
connection.commit()
connection.close()
