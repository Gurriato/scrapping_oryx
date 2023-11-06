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
def scrappingOryx():
    import hashlib
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    def generate_short_hash(row):
        hash_input = '_'.join([str(row['weapon']), str(row['platform']), str(row['number']), str(row['url'])])
        return hashlib.sha256(hash_input.encode()).hexdigest()[:20]  #

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

    # concat and final cleaning
    to_file = pd.concat([RU, UA])
    to_file = to_file.reset_index(drop=True)
    to_file['url'] = to_file['url'].apply(tools.clean_url)

    # Memory
    scraped_object, UA, RU = None, None, None
    gc.collect()

    to_file['primary_key'] = to_file.apply(generate_short_hash, axis=1)

    to_report = to_file.copy()
    to_report['Status'] = to_report['Status'].astype(str)
    to_report['origen'] = to_report['origen'].astype(str)
    outcome = tools.insertar_en_bbdd(to_report, config['usuario'], config['pass'], config['host'], config['database'], 'bajas')
    print(outcome)
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
    return to_file, total_UA, total_RU
def dataReport():
    from ydata_profiling import ProfileReport
    report = pd.read_csv(r'.\Data\scrap_raw.csv')
    profile = ProfileReport(report, title="Oryx Data Report")
    profile.to_file(r'.\informe.html')

def comparar_dataframes(df_a, df_b, df_excepciones):
    # Convertir las primary keys de excepciones en un set para rápida referencia
    excepciones_a = set(df_excepciones['primary_key_a'])
    excepciones_b = set(df_excepciones['primary_key_b'])

    # Filtrar df_b para excluir las filas que tienen primary keys en el set de excepciones
    df_b_filtrado = df_b[~df_b['primary_key'].isin(excepciones_b)]

    # Identificar las filas en df_b que no están en df_a
    df_a_keys = set(df_a['primary_key'])
    df_b_filtrado = df_b_filtrado[~df_b_filtrado['primary_key'].isin(df_a_keys)]

    return df_b_filtrado

# Aplicar la función a los DataFrames de ejemplo

if __name__ == '__main__':
    to_file, total_UA, total_RU = scrappingOryx()
    exceptions = pd.read_csv('./Data/exceptions.csv', sep=';')
    base = pd.read_csv('./Data/base.csv', sep=';')
    df_resultado = comparar_dataframes(base, to_file, exceptions) #nuevas lineas a incluir