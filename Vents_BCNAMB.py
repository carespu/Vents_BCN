
#importem la llibreria pandas i la matplotlib
import pandas as pd
import numpy as np

#read .csv with wind
vents = pd.read_csv('Dades_meteorol_giques_de_la_XEMA_AMB10anys.csv')

#read .csv with variable metadata
vari = pd.read_csv('Metadades_variables_meteo.csv')

#read .csv with estacions metadata
Estacio = pd.read_csv('Metadades_estacions_meteorol_giques_autom_tiques_AMB.csv')

# Join vents and vari per CODI_VARIABLE
df1 = pd.merge(vari, vents, on='CODI_VARIABLE')


# Join df1 and Estacio per CODI_ESTACIO
df2 = pd.merge(df1, Estacio, on='CODI_ESTACIO')

# select only columns of interest in a new df

df3 = df2[['CODI_ESTACIO','VARIABLE','DATA_LECTURA','VALOR_LECTURA','NOM_ESTACIO','LATITUD', 'LONGITUD', 'ALTITUD','CODI_VARIABLE']]



#convertir format hora AM/PM en 24 hours
df3["NEW_DATA_LECTURA"] = pd.to_datetime(df3["DATA_LECTURA"], format= '%d/%m/%Y %I:%M:%S %p')

# agrupar valors que no hem de transposar però que volem conservar en un dataframe 

ventsgrouped = df3.groupby(['CODI_ESTACIO','ALTITUD','LATITUD','LONGITUD','NOM_ESTACIO','DATA_LECTURA', 'NEW_DATA_LECTURA']).apply(', '.join).reset_index()

#transposar valors incloguent codi Estacio

#primer fem etiqueta de dataframe per tenir valors unics
df3['ESTACIO_DATA'] = df3['CODI_ESTACIO'] +'-'+ df3['DATA_LECTURA']


#Now data frame  transposat amb valors transposats per valor unic
dftr = df3.pivot(index='ESTACIO_DATA', columns='VARIABLE', values='VALOR_LECTURA')     

# Al fer el pas anterior hem creat un index Estacio_data, CONVERTIR INDEX EN COLUMNA
dftr.reset_index(inplace=True)
dftr

#Faig la columna ESTACIO_DATA per a l'altre df ventsgrouped, per poder fer el merge amb dftr
ventsgrouped['ESTACIO_DATA'] = ventsgrouped['CODI_ESTACIO'] +'-'+ ventsgrouped['DATA_LECTURA']

#MERGE el transposat i el resum
ventstr = pd.merge(dftr,ventsgrouped , on='ESTACIO_DATA')
ventstr


#crear dia mes i any en columnes separades
ventstr["diaMes"] = ventstr['NEW_DATA_LECTURA'].map(lambda x: x.day)
ventstr["Mes"] = ventstr['NEW_DATA_LECTURA'].map(lambda x: x.month)
ventstr["Any"] = ventstr['NEW_DATA_LECTURA'].map(lambda x: x.year)
ventstr['diaSet']=ventstr['NEW_DATA_LECTURA'].dt.weekday_name
ventstr['hora']=ventstr['NEW_DATA_LECTURA'].map(lambda x: x.hour)


#guardem .csv amb valors finals de l'exercisi
ventstr.to_csv("ventsfinal.csv")


                 