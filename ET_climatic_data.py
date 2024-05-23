# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

#Lire les fichiers CSV en tant que DataFrame

#ALGERIA

DZ_1=pd.read_csv("./Weather_Data//Algeria//Weather_1920-1929_ALGERIA.csv")
DZ_2=pd.read_csv("./Weather_Data//Algeria//Weather_1930-1939_ALGERIA.csv")
DZ_3=pd.read_csv("./Weather_Data//Algeria//Weather_1940-1949_ALGERIA.csv")
DZ_4=pd.read_csv("./Weather_Data//Algeria//Weather_1950-1959_ALGERIA.csv")
DZ_5=pd.read_csv("./Weather_Data//Algeria//Weather_1960-1969_ALGERIA.csv")
DZ_6=pd.read_csv("./Weather_Data//Algeria//Weather_1970-1979_ALGERIA.csv")
DZ_7=pd.read_csv("./Weather_Data//Algeria//Weather_1980-1989_ALGERIA.csv")
DZ_8=pd.read_csv("./Weather_Data//Algeria//Weather_1990-1999_ALGERIA.csv")
DZ_9=pd.read_csv("./Weather_Data//Algeria//Weather_2000-2009_ALGERIA.csv")
DZ_10=pd.read_csv("./Weather_Data//Algeria//Weather_2010-2019_ALGERIA.csv")
DZ_11=pd.read_csv("./Weather_Data//Algeria//Weather_2020-2022_ALGERIA.csv")




#MOROCCO

M_1=pd.read_csv("./Weather_Data//Morocco//Weather_1920-1959_MOROCCO.csv")
M_2=pd.read_csv("./Weather_Data//Morocco//Weather_1960-1989_MOROCCO.csv")
M_3=pd.read_csv("./Weather_Data//Morocco//Weather_1990-2019_MOROCCO.csv")
M_4=pd.read_csv("./Weather_Data//Morocco//Weather_2020-2022_MOROCCO.csv")



#TUNISIA

T_1=pd.read_csv("./Weather_Data//Tunisia//Weather_1920-1959_TUNISIA.csv")
T_2=pd.read_csv("./Weather_Data//Tunisia//Weather_1960-1989_TUNISIA.csv")
T_3=pd.read_csv("./Weather_Data//Tunisia//Weather_1990-2019_TUNISIA.csv")
T_4=pd.read_csv("./Weather_Data//Tunisia//Weather_2020-2022_TUNISIA.csv")





#L'Ajout des Attributs manquants dans chaque dataframe  (24 attributs)

# List des dataframes
dataframes = [DZ_1,DZ_2,DZ_3,DZ_4,DZ_5,DZ_6,DZ_7,DZ_8,DZ_9,DZ_10,DZ_11,M_1,M_2,M_3,M_4,T_1,T_2,T_3,T_4] 
# List des attributs requises
attributes_to_add = ["SNWD","SNOW","WDFG","PGTM","WSFG"]


for df in dataframes:
 
    # L'ajout des attributes s'il n'existent pas dans les dataframes 
    for attribute in attributes_to_add:
        if attribute not in df.columns:
            df[attribute] = np.nan 
            
    # Suppression des attributs non pertinents
    attributes_to_remove = [col for col in df.columns if col.endswith('_ATTRIBUTES') or col =="ACSH" or col=="WDFM" or col=="WSFM" or col.startswith('WT')]
    df.drop(columns=attributes_to_remove, inplace=True)
    




#Remplissage des valeurs manquantes en utilisant les differentes strategies (moyenne ,valeure precedante ,valeur prochaine)

#DZ 1
DZ_1[['PRCP','TMAX','TMIN']]=DZ_1[['PRCP','TMAX','TMIN']].bfill()


#DZ 2
DZ_2[['PRCP','TMAX','TMIN']]=DZ_2[['PRCP','TMAX','TMIN']].bfill()

#DZ 3
DZ_3[['PRCP','TMAX','TMIN','TAVG']]=DZ_3[['PRCP','TMAX','TMIN','TAVG']].fillna(DZ_3[['PRCP','TMAX','TMIN','TAVG']].mean())

#DZ 4
DZ_4[['PRCP','TMAX','TMIN','TAVG']]=DZ_4[['PRCP','TMAX','TMIN','TAVG']].fillna(DZ_4[['PRCP','TMAX','TMIN','TAVG']].mean())


#DZ 5
DZ_5[['PRCP','TMAX','TMIN','TAVG']]=DZ_5[['PRCP','TMAX','TMIN','TAVG']].fillna(DZ_5[['PRCP','TMAX','TMIN','TAVG']].mean())


#DZ 6
DZ_6[['PRCP','TMAX','TMIN','TAVG']]=DZ_6[['PRCP','TMAX','TMIN','TAVG']].fillna(DZ_6[['PRCP','TMAX','TMIN','TAVG']].mean())

#DZ 7
DZ_7[['PRCP','TMAX','TMIN','TAVG']]=DZ_7[['PRCP','TMAX','TMIN','TAVG']].fillna(DZ_7[['PRCP','TMAX','TMIN','TAVG']].mean())

#DZ 8
DZ_8[['PRCP','TMAX','TMIN','TAVG']]=DZ_8[['PRCP','TMAX','TMIN','TAVG']].fillna(DZ_8[['PRCP','TMAX','TMIN','TAVG']].mean())


#DZ 9
DZ_9[['PRCP','TMAX','TMIN']]=DZ_9[['PRCP','TMAX','TMIN']].fillna(DZ_9[['PRCP','TMAX','TMIN']].mean())


#DZ 10
DZ_10[['PRCP','TMAX','TMIN']]=DZ_10[['PRCP','TMAX','TMIN']].ffill()


#DZ 11
DZ_11[['PRCP','TMIN']]=DZ_11[['PRCP','TMIN']].bfill()


#M 1
M_1[['PGTM','WSFG','WDFG']]=M_1[['PGTM','WSFG','WDFG']].bfill()


#M 2
M_2[['PRCP','TMAX','TMIN','TAVG']]=M_2[['PRCP','TMAX','TMIN','TAVG']].fillna(M_2[['PRCP','TMAX','TMIN','TAVG']].mean())


# M 3
M_3[['PRCP','TMAX','TMIN','TAVG']]=M_3[['PRCP','TMAX','TMIN','TAVG']].ffill()

#M 4
M_4[['PRCP','TMAX','TMIN','TAVG']]=M_4[['PRCP','TMAX','TMIN','TAVG']].ffill()


#T 1
T_1[['PRCP','TMAX','TMIN']]=T_1[['PRCP','TMAX','TMIN']].fillna(T_1[['PRCP','TMAX','TMIN']].mean())

#T 2
T_2[['TAVG','TMAX','TMIN']]=T_2[['TAVG','TMAX','TMIN']].ffill()


#T 3
T_3[['PRCP','TMAX','TMIN']]=T_3[['PRCP','TMAX','TMIN']].bfill()


#T 4
T_4[['PRCP','TMAX','TMIN']]=T_4[['PRCP','TMAX','TMIN']].fillna(T_4[['PRCP','TMAX','TMIN']].mean())






# Réordonner les colonnes 

for i in range(len(dataframes)):
    dataframes[i] = dataframes[i].reindex(sorted(dataframes[i].columns), axis=1)

# Concaténer les DataFrames verticalement

climatic_df= pd.concat(dataframes, ignore_index=True)




# TRAITEMENT DE L'ATTRIBUTS DATE

# Extraire les autres composants de la date

climatic_df['DATE'] = pd.to_datetime(climatic_df['DATE'], format='%Y-%m-%d')
climatic_df['Full_date'] = climatic_df['DATE']
climatic_df['Day_Name'] = climatic_df['DATE'].dt.day_name()
climatic_df['Month'] = climatic_df['DATE'].dt.month
climatic_df['Mounth_Name'] = climatic_df['DATE'].dt.month_name()
climatic_df['year'] = climatic_df['DATE'].dt.year
climatic_df['quarter'] = climatic_df['DATE'].dt.to_period('Q').astype(str)
climatic_df['semester'] = (climatic_df['DATE'].dt.year.astype(str) + '-S' +
                    ((climatic_df['DATE'].dt.month-1) // 6 + 1).astype(str))

# Define function to get season



def get_season(month):
    if 3 <= month <= 5:
        return 'Spring'
    elif 6 <= month <= 8:
        return 'Summer'
    elif 9 <= month <= 11:
        return 'Fall'
    else:
        return 'Winter'

climatic_df['Season'] = climatic_df['DATE'].dt.month.apply(get_season)
climatic_df['WeekendFlag'] =climatic_df['Day_Name'].apply(lambda x: 1 if x in ['Friday', 'Saturday'] else 0)
climatic_df.drop('DATE', axis=1, inplace=True)



# Extraire le nom du pays

def get_country_name(name):
    # Diviser le nom par une virgule et supprimer les espaces des deux parties
    parts = [part.strip().upper() for part in name.split(',')]
    
   
    if 'AG' in parts:
        return 'Algeria'
    elif 'MO' in parts:
        return 'Morocco'
    elif 'SP' in parts:
        return 'Morocco'
    elif 'TS' in parts:
        return 'Tunisia'
    else:
        return None

# Créer la colonne 'country_name'
climatic_df['country_name'] = climatic_df['NAME'].apply(get_country_name)



file_path = "climatic_dataSet.csv"  
climatic_df.to_csv(file_path, index=False)



