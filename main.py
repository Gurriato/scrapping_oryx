# -*- coding: utf-8 -*-
"""
Este script tiene como objetivo raspar información de dos artículos específicos
sobre equipos de origen ruso y ucraniano. La información se extrae, transforma
y almacena en DataFrames de pandas.

Created on Wed Aug 23 14:24:10 2023
@author: gblancom
"""

import pandas as pd
import gc
import tools
import json
import datetime as dt
import re
from ydata_profiling import ProfileReport
import matplotlib


import configparser

with open('config.json', 'r') as config_file:
    config = json.load(config_file)


column_order = ['owner', 'origen', 'weapon', 'platform', 'total', 'number', 'Status', 'url']

# Russia scrap
urlRU = 'https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html'
scraped_object = tools.extract_lists_from_article(urlRU)
RU, total_RU = tools.trans_to_df(scraped_object)
RU['origen'] = RU['origen'].apply(tools.extr_country)
RU[['total', 'platform']] = RU['platform'].str.extract(r'(\d+)\s?([^:]+)', expand=True)
RU['owner'] = 'RU'
RU = RU[column_order]

# Ucrania scrap
urlUA = 'https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html'
scraped_object = tools.extract_lists_from_article(urlUA)
UA, total_UA = tools.trans_to_df(scraped_object)
UA['origen'] = UA['origen'].apply(tools.extr_country)
UA[['total', 'platform']] = UA['platform'].str.extract(r'(\d+)\s?([^:]+)', expand=True)
UA['owner'] = 'UA'
UA = UA[column_order]

to_file = pd.concat([RU, UA])
to_file = to_file.reset_index(drop=True)

# Memory
scraped_object, UA, RU = None, None, None
gc.collect()


to_report = to_file.copy()
to_report['Status'] = to_report['Status'].astype(str)
to_report['origen'] = to_report['origen'].astype(str)
outcome = tools.insertar_en_bbdd(to_report, config['usuario'], config['pass'], config['host'], config['database'], 'bajas')
now = dt.datetime.now()
to_file.to_csv('./Data/scrap_raw_' + str(now.date()) + '.csv')

# Transforming Totals
regex = r"^(.+?)\s*\((\d+), of which( destroyed: (\d+))?(, damaged: (\d+))?(, abandoned: (\d+))?(, captured: (\d+))?\)$"
total_RU = pd.Series(total_RU)
total_RU = total_RU.str.extract(regex)
total_RU.columns = ['Type', 'Total', 'd1', 'Destroyed', 'd2', 'Damaged', 'd3', 'Abandoned', 'd4', 'Captured']
total_RU.drop(['d1', 'd2', 'd3', 'd4'], axis=1, inplace=True)
total_RU = total_RU[1:]
total_RU.fillna(0, inplace=True)
total_RU[['Total', 'Destroyed', 'Damaged', 'Abandoned', 'Captured']] = total_RU[['Total', 'Destroyed', 'Damaged', 'Abandoned', 'Captured']].astype(int)
outcome = tools.insertar_en_bbdd(total_RU, config['usuario'], config['pass'], config['host'], config['database'], 'totals_RU')
total_RU.to_csv('./Data/scrap_Total_RU' + str(now.date()) + '.csv')

total_UA = pd.Series(total_UA)
total_UA = total_UA.str.extract(regex)
total_UA.columns = ['Type', 'Total', 'd1', 'Destroyed', 'd2', 'Damaged', 'd3', 'Abandoned', 'd4', 'Captured']
total_UA.drop(['d1', 'd2', 'd3', 'd4'], axis=1, inplace=True)
total_UA = total_UA[1:]
total_UA.fillna(0, inplace=True)
total_UA[['Total', 'Destroyed', 'Damaged', 'Abandoned', 'Captured']] = total_UA[['Total', 'Destroyed', 'Damaged', 'Abandoned', 'Captured']].astype(int)
outcome = tools.insertar_en_bbdd(total_UA, config['usuario'], config['pass'], config['host'], config['database'], 'totals_UA')
total_UA.to_csv('./Data/scrap_Total_UA_' + str(now.date()) + '.csv')


#z = pd.read_html('./z.html')
#tables = tools.extract_tables_from_url2("https://bmpvsu.ru/z.php")
#tables = tools.extract_tables_from_url("https://bmpvsu.ru/z.php", cookies={"cf_clearance": "lfDdB.0GNEjY4GMTL.K.SW2t0G8ygAKv26aSmv_yJHc-1698680237-0-1-f12dae8d.8e7db428.a62cf16d-160.0.0"}, referer="https://www.google.com")

#from ydata_profiling import ProfileReport
#report = pd.read_csv(r'C:\Users\gblancom\PycharmProjects\pythonProject\scrap_raw.csv')
#profile = ProfileReport(report, title="Informe de perfil de pandas")
#profile.to_file(r'C:\Users\gblancom\PycharmProjects\pythonProject\informe.html')


df_ext = pd.read_csv('./Data/2023-10-27.csv')

import numpy as np
cjt1 = pd.Series(to_file['url'].unique())
cjt1 = cjt1.apply(limpiar_url)
cjt2 = pd.Series(df_ext['url'].unique())
cjt2 = cjt2.apply(limpiar_url)
# Calculamos la diferencia simétrica
no_comunes = set(cjt1).symmetric_difference(set(cjt2))
data = []

# Iterar sobre cada valor en no_comunes
for valor in no_comunes:
    # Verificar si el valor está en cada conjunto
    en_cjt1 = valor in cjt1.values
    en_cjt2 = valor in cjt2.values

    # Obtener los índices si el valor está presente
    indice_cjt1 = cjt1[cjt1 == valor].index.tolist()
    indice_cjt2 = cjt2[cjt2 == valor].index.tolist()

    # Añadir la información al DataFrame
    data.append({
        'En_cjt1': en_cjt1,
        'Indice_cjt1': indice_cjt1[0] if indice_cjt1 else np.nan,
        'En_cjt2': en_cjt2,
        'Indice_cjt2': indice_cjt2[0] if indice_cjt2 else np.nan,
        'Valor': valor
    })

# Convertir la lista en un DataFrame
df_resultado = pd.DataFrame(data)

# Convertir los índices a integer
df_resultado['Indice_cjt1'] = df_resultado['Indice_cjt1'].astype('Int64')
df_resultado['Indice_cjt2'] = df_resultado['Indice_cjt2'].astype('Int64')

# Crear conjunto de índices combinados y ordenar por él
df_resultado['Indices_combinados'] = df_resultado['Indice_cjt1'].combine_first(df_resultado['Indice_cjt2'])
df_resultado.sort_values(by='Indices_combinados', inplace=True)
df_resultado.drop(columns='Indices_combinados', inplace=True)


def limpiar_url(url):
    # Eliminar espacios al principio y al final
    url = url.strip()

    # Reemplazar tabulaciones con espacios vacíos
    url = url.replace('\t', '')

    return url


# Aplicar la función limpiar_url a cada elemento en cjt1
cjt1_limpiado = cjt1.apply(limpiar_url)