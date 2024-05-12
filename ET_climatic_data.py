# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np



#ALGERIA

DZ_1=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Algeria//Weather_1920-1929_ALGERIA.csv")
DZ_2=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Algeria//Weather_1930-1939_ALGERIA.csv")
DZ_3=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Algeria//Weather_1940-1949_ALGERIA.csv")
DZ_4=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Algeria//Weather_1950-1959_ALGERIA.csv")
DZ_5=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Algeria//Weather_1960-1969_ALGERIA.csv")
DZ_6=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Algeria//Weather_1970-1979_ALGERIA.csv")
DZ_7=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Algeria//Weather_1980-1989_ALGERIA.csv")
DZ_8=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Algeria//Weather_1990-1999_ALGERIA.csv")
DZ_9=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Algeria//Weather_2000-2009_ALGERIA.csv")
DZ_10=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Algeria//Weather_2010-2019_ALGERIA.csv")
DZ_11=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Algeria//Weather_2020-2022_ALGERIA.csv")




#MOROCCO

M_1=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Morocco//Weather_1920-1959_MOROCCO.txt")
M_2=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Morocco//Weather_1960-1989_MOROCCO.csv")
M_3=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Morocco//Weather_1990-2019_MOROCCO.csv")
M_4=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Morocco//Weather_2020-2022_MOROCCO.csv")



#TUNISIA

T_1=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Tunisia//Weather_1920-1959_TUNISIA.csv")
T_2=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Tunisia//Weather_1960-1989_TUNISIA.csv")
T_3=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Tunisia//Weather_1990-2019_TUNISIA.csv")
T_4=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//Dataset//Weather_Data//Tunisia//Weather_2020-2022_TUNISIA.csv")





#L'Ajout des Attributs manquants dans chaque dataframe  (24 attributs)

# List des dataframes
dataframes = [DZ_1,DZ_2,DZ_3,DZ_4,DZ_5,DZ_6,DZ_7,DZ_8,DZ_9,DZ_10,DZ_11,M_1,M_2,M_3,M_4,T_1,T_2,T_3,T_4] 
# List des attributs requises
attributes_to_add = ["SNWD","SNOW","WDFG","PGTM","WSFG","WT01","WT02","WT03","WT05","WT07","WT08","WT09","WT16","WT18"]


for df in dataframes:
 
    # Add new attributes if they do not exist
    for attribute in attributes_to_add:
        if attribute not in df.columns:
            df[attribute] = np.nan 
            
    attributes_to_remove = [col for col in df.columns if col.endswith('_ATTRIBUTES') or col =="ACSH" or col=="WDFM" or col=="WSFM"]
    df.drop(columns=attributes_to_remove, inplace=True)
    




#Remplissage des valeurs manquantes 

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
#SNWD         128059 /128258 99%

#DZ 9
DZ_9[['PRCP','TMAX','TMIN']]=DZ_9[['PRCP','TMAX','TMIN']].fillna(DZ_9[['PRCP','TMAX','TMIN']].mean())
#SNWD         186098 /186537 99%

#DZ 10
DZ_10[['PRCP','TMAX','TMIN']]=DZ_10[['PRCP','TMAX','TMIN']].ffill()
#SNWD         190760 / 191302 99%

#DZ 11
DZ_11[['PRCP','TMIN']]=DZ_11[['PRCP','TMIN']].bfill()
# SNWD         44661  /44694  99%
# TMAX         41373 /44694  92%

#M 1
M_1[['PGTM','WSFG','WDFG']]=M_1[['PGTM','WSFG','WDFG']].bfill()



#M 2
M_2[['PRCP','TMAX','TMIN','TAVG']]=M_2[['PRCP','TMAX','TMIN','TAVG']].fillna(M_2[['PRCP','TMAX','TMIN','TAVG']].mean())
# PGTM          96613/103586 93%
# SNOW          96475/103586 93%
# SNWD          96379/103586 93%
# WDFG          96613/103586 93%
# WSFG          96611/103586 93%

# M 3
M_3[['PRCP','TMAX','TMIN','TAVG']]=M_3[['PRCP','TMAX','TMIN','TAVG']].ffill()
#SNWD         127109/127111 99.99%

#M 4
M_4[['PRCP','TMAX','TMIN','TAVG']]=M_4[['PRCP','TMAX','TMIN','TAVG']].ffill()
#SNWD         11056/11059  99.99%

#T 1
T_1[['PRCP','TMAX','TMIN']]=T_1[['PRCP','TMAX','TMIN']].fillna(T_1[['PRCP','TMAX','TMIN']].mean())
#TAVG         68630/71409  96.1%

#T 2
T_2[['TAVG','TMAX','TMIN']]=T_2[['TAVG','TMAX','TMIN']].ffill()
#PRCP         22618/37228  60.75%
#SNWD         37226/37228  99.99%



#T 3
T_3[['PRCP','TMAX','TMIN']]=T_3[['PRCP','TMAX','TMIN']].bfill()
#SNWD         54486/54488   99.99%


#T 4
T_4[['PRCP','TMAX','TMIN']]=T_4[['PRCP','TMAX','TMIN']].fillna(T_4[['PRCP','TMAX','TMIN']].mean())



# TRAITEMENT DE L'ATTRIBUTS WT**
WT = ["WT01", "WT02", "WT03", "WT05", "WT07", "WT08", "WT09", "WT16", "WT18"]

for df in dataframes:
    df[WT] = df[WT].fillna(0)





# Reorder the columns and merge them in the same dataframe

for i in range(len(dataframes)):
    dataframes[i] = dataframes[i].reindex(sorted(dataframes[i].columns), axis=1)

# Concatenate the DataFrames vertically
climatic_dataSet= pd.concat(dataframes, ignore_index=True)
climatic_dataSet.to_csv('C:/Users/Dell/Documents/M1_ISII/S2/DataWarehouse/climatic_dataSet.csv', index=False)


print(climatic_dataSet.isnull().sum())
check_climatic_csv=pd.read_csv("C://Users//Dell//Documents//M1_ISII//S2//DataWarehouse//climatic_dataSet.csv")

